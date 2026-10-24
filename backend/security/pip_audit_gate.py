"""Fail CI when pip-audit finds a high or critical vulnerability.

pip-audit 2.10 lists vulnerabilities and does not include a severity.
This module asks OSV for each id. A GitHub label on the OSV record is
used when it is present. Otherwise the CVSS v3 base score is calculated
from the vector. 7.0 and above is high. 9.0 and above is critical.

A finding with no severity fails the build. Missing data is not treated
as safe. Low and moderate findings are left for a human to read; they do
not fail the build.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from decimal import ROUND_CEILING, Decimal

OSV_VULN_URL = "https://api.osv.dev/v1/vulns/"
BLOCKING_LEVELS = frozenset({"HIGH", "CRITICAL", "UNKNOWN"})
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,80}$")

# CVSS v3.1 specification, section 7.1. Values are the ones in the spec.
_AV = {"N": "0.85", "A": "0.62", "L": "0.55", "P": "0.2"}
_AC = {"L": "0.77", "H": "0.44"}
_UI = {"N": "0.85", "R": "0.62"}
_PR_UNCHANGED = {"N": "0.85", "L": "0.62", "H": "0.27"}
_PR_CHANGED = {"N": "0.85", "L": "0.68", "H": "0.5"}
_CIA = {"H": "0.56", "L": "0.22", "N": "0"}
_LABELS = frozenset({"NONE", "LOW", "MODERATE", "MEDIUM", "HIGH", "CRITICAL"})

Fetcher = Callable[[str], dict | None]


@dataclass(frozen=True)
class Finding:
    """One vulnerability from the pip-audit report, with a severity label."""

    package: str
    version: str
    vuln_id: str
    level: str


def _round_up(value: Decimal) -> float:
    """CVSS Roundup: ceiling to one decimal place."""
    rounded = value.quantize(Decimal("0.1"), rounding=ROUND_CEILING)
    return float(rounded)


def cvss_v3_base_score(vector: str) -> float | None:
    """Return the CVSS v3 base score, or None when the vector is not v3."""
    if not vector.startswith("CVSS:3"):
        return None
    metrics: dict[str, str] = {}
    for part in vector.split("/")[1:]:
        if ":" not in part:
            return None
        key, _, raw = part.partition(":")
        metrics[key] = raw
    try:
        attack = Decimal(_AV[metrics["AV"]])
        complexity = Decimal(_AC[metrics["AC"]])
        interaction = Decimal(_UI[metrics["UI"]])
        scope_changed = metrics["S"] == "C"
        privileges = Decimal(
            (_PR_CHANGED if scope_changed else _PR_UNCHANGED)[metrics["PR"]]
        )
        confidentiality = Decimal(_CIA[metrics["C"]])
        integrity = Decimal(_CIA[metrics["I"]])
        availability = Decimal(_CIA[metrics["A"]])
    except KeyError:
        return None

    exploitability = Decimal("8.22") * attack * complexity * privileges * interaction
    impact_base = Decimal(1) - (
        (Decimal(1) - confidentiality)
        * (Decimal(1) - integrity)
        * (Decimal(1) - availability)
    )
    if scope_changed:
        impact = (
            Decimal("7.52") * (impact_base - Decimal("0.029"))
            - Decimal("3.25") * (impact_base - Decimal("0.02")) ** 15
        )
    else:
        impact = Decimal("6.42") * impact_base
    if impact <= 0:
        return 0.0
    if scope_changed:
        raw = min(Decimal("1.08") * (impact + exploitability), Decimal(10))
    else:
        raw = min(impact + exploitability, Decimal(10))
    return _round_up(raw)


def level_from_score(score: float) -> str:
    if score <= 0:
        return "NONE"
    if score < 4:
        return "LOW"
    if score < 7:
        return "MEDIUM"
    if score < 9:
        return "HIGH"
    return "CRITICAL"


def level_from_osv(document: dict) -> str:
    """Read a GitHub severity label, then a CVSS v3 vector."""
    database = document.get("database_specific") or {}
    if isinstance(database, dict):
        label = str(database.get("severity") or "").upper()
        if label in _LABELS:
            return "MEDIUM" if label == "MODERATE" else label

    for entry in document.get("severity") or []:
        if not isinstance(entry, dict):
            continue
        score_text = str(entry.get("score") or "")
        kind = str(entry.get("type") or "")
        if kind.startswith("CVSS_V3") or score_text.startswith("CVSS:3"):
            score = cvss_v3_base_score(score_text)
            if score is not None:
                return level_from_score(score)
    return "UNKNOWN"


def _candidate_ids(vuln: dict) -> list[str]:
    primary = str(vuln.get("id") or "")
    aliases = [str(alias) for alias in vuln.get("aliases") or []]
    ordered: list[str] = []
    for vuln_id in [*aliases, primary]:
        if vuln_id.startswith("GHSA-") and vuln_id not in ordered:
            ordered.append(vuln_id)
    for vuln_id in [primary, *aliases]:
        if vuln_id and vuln_id not in ordered:
            ordered.append(vuln_id)
    return ordered


def _level_for_vuln(vuln: dict, fetch: Fetcher) -> str:
    for vuln_id in _candidate_ids(vuln):
        document = fetch(vuln_id)
        if not document:
            continue
        level = level_from_osv(document)
        if level != "UNKNOWN":
            return level
    return "UNKNOWN"


def classified_findings(report: dict, fetch: Fetcher) -> list[Finding]:
    """Return every vulnerability with a severity label."""
    found: list[Finding] = []
    for dependency in report.get("dependencies") or []:
        package = str(dependency.get("name") or "")
        version = str(dependency.get("version") or "")
        for vuln in dependency.get("vulns") or []:
            found.append(
                Finding(
                    package=package,
                    version=version,
                    vuln_id=str(vuln.get("id") or ""),
                    level=_level_for_vuln(vuln, fetch),
                )
            )
    return found


def blocking_findings(report: dict, fetch: Fetcher) -> list[Finding]:
    """Return findings that should fail the build."""
    return [
        finding
        for finding in classified_findings(report, fetch)
        if finding.level in BLOCKING_LEVELS
    ]


def fetch_osv(vuln_id: str) -> dict | None:
    """Load one OSV record. A 404 is an unknown id. Other errors propagate."""
    if not _ID_RE.fullmatch(vuln_id):
        return None
    request = urllib.request.Request(
        OSV_VULN_URL + vuln_id,
        headers={
            "Accept": "application/json",
            "User-Agent": "rolefit-pip-audit-gate",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    document = json.loads(payload)
    if not isinstance(document, dict):
        return None
    return document


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv if argv is None else argv)
    if len(args) != 2:
        print(
            "usage: python -m security.pip_audit_gate REPORT.json",
            file=sys.stderr,
        )
        return 2
    try:
        with open(args[1], encoding="utf-8") as handle:
            report = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        print(f"pip-audit report is missing or not JSON: {error}", file=sys.stderr)
        return 1
    if not isinstance(report, dict):
        print(
            "pip-audit report is missing or not JSON: expected an object",
            file=sys.stderr,
        )
        return 1
    try:
        found = classified_findings(report, fetch_osv)
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as error:
        print(f"could not look up severity on OSV: {error}", file=sys.stderr)
        return 1
    blocking = [finding for finding in found if finding.level in BLOCKING_LEVELS]
    noted = [finding for finding in found if finding.level not in BLOCKING_LEVELS]
    if noted:
        print("low or moderate Python vulnerabilities (these do not fail CI):")
        for finding in noted:
            print(
                f"  {finding.package} {finding.version} "
                f"{finding.vuln_id} {finding.level}"
            )
    if blocking:
        print("high or critical Python vulnerabilities:")
        for finding in blocking:
            print(
                f"  {finding.package} {finding.version} "
                f"{finding.vuln_id} {finding.level}"
            )
        return 1
    print("no high or critical Python vulnerabilities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

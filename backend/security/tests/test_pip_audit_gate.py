import json

from security.pip_audit_gate import (
    blocking_findings,
    classified_findings,
    cvss_v3_base_score,
    level_from_osv,
)


def test_cvss_v3_scores_match_the_spec() -> None:
    assert cvss_v3_base_score("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H") == 9.8
    assert cvss_v3_base_score("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H") == 8.8
    assert cvss_v3_base_score("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N") == 6.1
    assert cvss_v3_base_score("CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N") == 3.1


def test_github_severity_label_wins_over_the_vector() -> None:
    document = {
        "database_specific": {"severity": "LOW"},
        "severity": [
            {"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}
        ],
    }

    assert level_from_osv(document) == "LOW"


def test_a_vector_is_used_when_there_is_no_label() -> None:
    document = {
        "severity": [
            {"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}
        ]
    }

    assert level_from_osv(document) == "CRITICAL"


def test_clean_report_does_not_ask_osv() -> None:
    def fetch(_vuln_id: str) -> dict:
        raise AssertionError("OSV should not be called")

    report = {"dependencies": [{"name": "django", "version": "5.2.18", "vulns": []}]}

    assert blocking_findings(report, fetch) == []


def test_high_finding_fails_and_moderate_does_not() -> None:
    documents = {
        "GHSA-high": {"database_specific": {"severity": "HIGH"}},
        "GHSA-moderate": {"database_specific": {"severity": "MODERATE"}},
    }

    def fetch(vuln_id: str) -> dict | None:
        return documents.get(vuln_id)

    report = {
        "dependencies": [
            {
                "name": "django",
                "version": "4.2.0",
                "vulns": [
                    {"id": "PYSEC-high", "aliases": ["GHSA-high"]},
                    {"id": "PYSEC-moderate", "aliases": ["GHSA-moderate"]},
                ],
            }
        ]
    }

    classified = classified_findings(report, fetch)
    blocking = blocking_findings(report, fetch)

    assert [item.level for item in classified] == ["HIGH", "MEDIUM"]
    assert [item.vuln_id for item in blocking] == ["PYSEC-high"]
    assert blocking[0].level == "HIGH"


def test_missing_severity_fails_closed() -> None:
    def fetch(_vuln_id: str) -> dict:
        return {"id": "PYSEC-unknown"}

    report = {
        "dependencies": [
            {"name": "django", "version": "1.0", "vulns": [{"id": "PYSEC-unknown"}]}
        ]
    }

    blocking = blocking_findings(report, fetch)

    assert [item.level for item in blocking] == ["UNKNOWN"]


def test_main_passes_a_clean_report(tmp_path, capsys) -> None:
    from security.pip_audit_gate import main

    report = tmp_path / "audit.json"
    report.write_text(json.dumps({"dependencies": []}), encoding="utf-8")

    assert main(["pip_audit_gate", str(report)]) == 0
    assert "no high or critical" in capsys.readouterr().out


def test_main_rejects_a_missing_report(capsys) -> None:
    from security.pip_audit_gate import main

    assert main(["pip_audit_gate", "/tmp/does-not-exist-rolefit-audit.json"]) == 1
    assert "report" in capsys.readouterr().err.lower()

"""Liveness endpoint for the scaffold.

This check does not query Postgres. A database outage should not make
the process look dead; a readiness check can be added when models exist.
"""

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
def health(_request: Request) -> Response:
    return Response({"status": "ok"})

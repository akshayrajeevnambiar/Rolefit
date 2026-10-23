"""Liveness endpoint for the scaffold.

This check does not query Postgres. A database outage should not make
the process look dead; a readiness check can be added when models exist.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(_request: Request) -> Response:
    return Response({"status": "ok"})

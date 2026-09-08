from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.views.decorators.http import require_safe
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.accounts.permissions import HasVerifiedAccount

from .registry import MODULES


@require_safe
def health(request):
    return JsonResponse({"status": "ok"})


@require_safe
def readiness(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({"service": "OOKULAR", "api_version": "v1", "stage": "foundation"})


@api_view(["GET"])
@permission_classes([IsAdminUser, HasVerifiedAccount])
def module_catalog(request):
    """Internal development map; planned modules expose no business endpoints."""
    return Response({"stage": "foundation", "modules": MODULES})

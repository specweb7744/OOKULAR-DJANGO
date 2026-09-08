from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def me(request):
    """Return only the caller's account; never accept an arbitrary user ID here."""
    return Response(
        {
            "id": str(request.user.pk),
            "email": request.user.email,
            "roles": list(request.user.roles.order_by("role").values_list("role", flat=True)),
        }
    )

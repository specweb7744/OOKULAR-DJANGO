from allauth.account.models import EmailAddress
from allauth.core import ratelimit
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_safe
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.profiles.permissions import is_employee
from apps.profiles.services import get_draft

from .forms import ResendVerificationForm
from .permissions import has_verified_email


@require_safe
def entrance(request):
    return redirect("account_home" if request.user.is_authenticated else "account_login")


@login_required
@require_safe
def account_home(request):
    if not has_verified_email(request.user):
        return render(request, "account/verified_email_required.html", status=403)
    employee = is_employee(request.user)
    return render(
        request,
        "accounts/home.html",
        {
            "roles": request.user.roles.order_by("role"),
            "is_employee": employee,
            "employee_profile": get_draft(request.user) if employee else None,
        },
    )


def send_verification_again(request, email):
    """Generic response; only an active unverified account receives a message."""
    if not ratelimit.consume(request, action="resend_verification", key=email):
        return False
    if ratelimit.consume(request, action="confirm_email", key=email):
        address = (
            EmailAddress.objects.filter(email__iexact=email, verified=False, user__is_active=True)
            .select_related("user")
            .first()
        )
        if address:
            address.send_confirmation(request)
    return True


@require_http_methods(["GET", "POST"])
def resend_verification(request):
    form = ResendVerificationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        if not send_verification_again(request, form.cleaned_data["email"].lower()):
            return ratelimit.respond_429(request)
        return redirect("account_email_verification_sent")
    return render(request, "accounts/resend_verification.html", {"form": form})


def csrf_failure(request, reason=""):
    return render(request, "403_csrf.html", status=403)


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

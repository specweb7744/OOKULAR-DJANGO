from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.accounts.permissions import HasVerifiedAccount, has_verified_email

from .forms import EmployeeProfileForm
from .models import EDITABLE_FIELDS
from .permissions import IsEmployee, is_employee
from .serializers import EmployeeProfilePatchSerializer
from .services import CONFLICT_MESSAGE, DraftConflict, draft_data, get_draft, save_draft


@login_required
@require_http_methods(["GET", "HEAD", "POST"])
def employee_profile(request):
    if not has_verified_email(request.user):
        return render(request, "account/verified_email_required.html", status=403)
    if not is_employee(request.user):
        return render(request, "profiles/employee_required.html", status=403)
    profile = get_draft(request.user)
    form = EmployeeProfileForm(
        request.POST if request.method == "POST" else None,
        initial=draft_data(profile),
    )
    status = 200
    conflict = False
    if request.method == "POST":
        if form.is_valid():
            try:
                save_draft(
                    request.user,
                    revision=form.cleaned_data["revision"],
                    data={field: form.cleaned_data[field] for field in EDITABLE_FIELDS},
                )
            except DraftConflict:
                form.add_error(None, CONFLICT_MESSAGE)
                conflict = True
                status = 409
            else:
                messages.success(request, "Szkic zapisany. Możesz wrócić do niego później.")
                return redirect("employee_profile")
        else:
            status = 400
    return render(
        request,
        "profiles/edit.html",
        {"form": form, "profile": profile, "conflict": conflict},
        status=status,
    )


@api_view(["GET", "HEAD", "PATCH"])
@permission_classes([HasVerifiedAccount, IsEmployee])
@parser_classes([JSONParser])
def my_employee_profile(request):
    if request.method in ("GET", "HEAD"):
        return Response(draft_data(get_draft(request.user)))
    serializer = EmployeeProfilePatchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = dict(serializer.validated_data)
    revision = data.pop("revision")
    try:
        profile = save_draft(request.user, revision=revision, data=data)
    except DraftConflict:
        current = get_draft(request.user)
        return Response(
            {
                "code": "draft_conflict",
                "detail": "Szkic został zmieniony. Pobierz aktualną wersję przed kolejnym zapisem.",
                "current_revision": current.revision if current else 0,
            },
            status=409,
        )
    return Response(draft_data(profile))

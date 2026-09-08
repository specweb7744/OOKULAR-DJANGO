from allauth.core import ratelimit
from allauth.headless.account.inputs import SignupInput
from allauth.headless.account.views import SignupView
from allauth.headless.base.views import APIView
from allauth.headless.internal.restkit.inputs import Input
from allauth.headless.internal.restkit.response import APIResponse

from .forms import AtomicSignupMixin, ResendVerificationForm
from .views import send_verification_again


class MobileSignupInput(AtomicSignupMixin, SignupInput):
    pass


class MobileSignupView(SignupView):
    input_class = {"POST": MobileSignupInput}


class MobileResendInput(ResendVerificationForm, Input):
    pass


class MobileResendView(APIView):
    input_class = {"POST": MobileResendInput}

    def post(self, request, *args, **kwargs):
        if not send_verification_again(request, self.input.cleaned_data["email"].lower()):
            return ratelimit.respond_429(request)
        return APIResponse(request)

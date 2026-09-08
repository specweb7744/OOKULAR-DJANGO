from types import SimpleNamespace

from allauth.headless import app_settings
from django.contrib.auth import get_user
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MobileSessionAuthentication(BaseAuthentication):
    """Validate expiry AND Django's auth hash, including after password resets."""

    def authenticate(self, request):
        token = request.headers.get("X-Session-Token")
        if not token:
            return None
        session = app_settings.TOKEN_STRATEGY.lookup_session(token)
        if session is not None:
            user = get_user(SimpleNamespace(session=session))
            if user.is_authenticated and user.is_active:
                return user, session
        raise AuthenticationFailed("Sesja wygasła. Zaloguj się ponownie.")

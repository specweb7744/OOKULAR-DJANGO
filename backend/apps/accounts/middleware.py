from django.utils.cache import patch_cache_control


class PrivateAccountPagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(("/konta/", "/konto/", "/api/auth/", "/api/v1/me/")):
            patch_cache_control(response, private=True, no_store=True, max_age=0)
            response["Referrer-Policy"] = "no-referrer"
        return response

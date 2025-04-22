from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ["/auth/login/", "/auth/register/", "/auth/forgot_password/"]
        if not request.user.is_authenticated and request.path not in public_paths:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)

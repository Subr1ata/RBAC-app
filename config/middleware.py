from django.shortcuts import redirect
from django.conf import settings
from apps.clients.models import Client
from django.http import JsonResponse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = ["/auth/login/", "/auth/register/", "/auth/forgot_password/"]
        if not request.user.is_authenticated and request.path not in public_paths:
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)

class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware called", request.user)
        api_key = request.headers.get('X-Client-API-Key')
        if api_key:
            client = Client.objects.filter(api_key=api_key).first()
            if client:
                request.client = client
            else:
                return JsonResponse({'success': False, 'error': 'Invalid API key'}, status=403)
        else:
            request.client = None
        return self.get_response(request)

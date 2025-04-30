from web_project import TemplateLayout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegistrationForm
import uuid
from apps.social_config.models import Client
from django.http import JsonResponse

def register_client(request):
    template_name = "register_client.html"
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.api_key = str(uuid.uuid4())  # Generate a unique API key
            client.save()
            messages.success(request, "Client registered successfully!")
            return redirect('register_client')
    else:
        form = ClientRegistrationForm()

    context = {
        'form': form
    }

    context = TemplateLayout().init(context)

    return render(request, template_name, context)


def get_client_social_integrations(request):
    client_api_key = request.headers.get('X-Client-API-Key')  # Pass API key in headers
    client = Client.objects.filter(api_key=client_api_key).first()

    if not client:
        return JsonResponse({'success': False, 'error': 'Invalid API key'}, status=403)

    social_integrations = client.social_integrations.all()
    return JsonResponse({'success': True, 'integrations': list(social_integrations.values())})

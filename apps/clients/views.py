from web_project import TemplateLayout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ClientRegistrationForm
import uuid
from apps.social_config.models import Client
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

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

def registered_clients(request):
    template_name = "registered_clients.html"
    form = ClientRegistrationForm()
    clients = Client.objects.all()  # Fetch all registered clients

    # Add pagination (optional)
    paginator = Paginator(clients, 10)  # Show 10 clients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
    }

    context = TemplateLayout().init(context)

    return render(request, template_name, context)

@csrf_exempt
def add_client_ajax(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.api_key = str(uuid.uuid4())  # Generate a unique API key
            client.save()
            return JsonResponse({'success': True, 'message': 'Client added successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def delete_client_ajax(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        messages.success(request, "Client deleted successfully!")
        return JsonResponse({'success': True, 'message': 'Client deleted successfully!'})
    messages.error(request, "Something went wrong!")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def update_client_ajax(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, id=client_id)
        form = ClientRegistrationForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully!")
            return JsonResponse({'success': True, 'message': 'Client updated successfully!'})
        else:
            messages.error(request, f"Something went wrong! Errors: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    messages.error(request, "Invalid request method.")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@csrf_exempt
def get_client_ajax(request, client_id):
    if request.method == 'GET':
        try:
            client = get_object_or_404(Client, id=client_id)
            client_data = {
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'business_name': client.business_name,
                'phone_number': client.phone_number,
                'address': client.address,
            }
            return JsonResponse({'success': True, 'client': client_data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error retrieving client: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
    # return JsonResponse({'success': False, 'message': 'Invalid request method.'})

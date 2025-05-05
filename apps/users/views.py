from web_project import TemplateLayout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CustomUser
from apps.authentication.models import Role
from apps.clients.models import Client
# from .models import CustomUser

def view_users(request):
    template_name = "view_users.html"

    if request.user.is_superuser:
        # Superuser can see all users
        users = CustomUser.objects.all().prefetch_related('roles', 'client')
    else:
        # Non-superusers can only see users belonging to their client
        if hasattr(request.user, 'client') and request.user.client:
            users = CustomUser.objects.filter(client=request.user.client).prefetch_related('roles', 'client')
        else:
            # If the logged-in user does not have a client, return an empty queryset
            users = CustomUser.objects.none()

    # Initial context
    context = {
        "users": users,
    }

    # Apply template layout enhancements (adds layout_path and other mappings)
    context = TemplateLayout().init(context)

    return render(request, template_name, context)

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            print(f"User '{user.username}' created successfully.")
            role = request.POST.get('role')

            # Assign the client to the user
            if request.user.is_superuser:
                client_id = request.POST.get('client')  # Get the client ID from the form
                print('create_user client_id -> ', client_id)  # Debug the client ID
                if client_id:
                    try:
                        user.client = Client.objects.get(id=client_id)
                    except Client.DoesNotExist:
                        messages.error(request, f"Client with ID '{client_id}' does not exist.")
                        return redirect('/users/create/')
            else:
                user.client = request.user.client  # Assign the current user's client if no valid client ID is provided

            user.save()  # Save the user to the database

            if role:
                print(f"Role selected: {role}")
                try:
                    custom_role = Role.objects.get(name=role)
                    user.roles.add(custom_role)
                    print(f"Role '{custom_role.name}' assigned to user '{user.username}'.")
                except Role.DoesNotExist:
                    print(f"Role '{role}' does not exist.")
                    messages.error(request, f"Role '{role}' does not exist.")
            print(f"User '{user.username}' saved to the database.")
            messages.success(request, "User created successfully!")
            return redirect('/users/list/')
    else:
        form = CustomUserCreationForm(user=request.user)

    roles = Role.objects.all()

    # Initial context
    context = {'form': form, 'roles': roles}

    if request.user.is_superuser:
        context['clients'] = Client.objects.all()

    # Apply template layout enhancements (adds layout_path and other mappings)
    context = TemplateLayout().init(context)
    return render(request, 'create_user.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, f"User '{user.username}' has been deleted.")
        return redirect("view_users")
    return redirect("view_users")

def edit_user(request, user_id):
    # User = get_user_model()  # Use the custom user model
    user = get_object_or_404(CustomUser, id=user_id)  # Fetch the user by ID

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user,  user=request.user)
        if form.is_valid():
            form.save()
            role_id = request.POST.get('role')
            if role_id:
                group = Role.objects.get(pk=role_id)
                user.roles.clear()  # Clear existing roles
                user.roles.add(group)  # Assign the selected role
            messages.success(request, "User updated successfully!")
            return redirect('/users/list/')
    else:
        form = CustomUserEditForm(instance=user, user=request.user)

    roles = Role.objects.all()
    user_roles = user.roles.values_list('id', flat=True)  # Get the IDs of the user's roles
    clients = Client.objects.all() if request.user.is_superuser else None

    # Initial context
    context = {
        'form': form,
        'roles': roles,
        'user': user,
        'user_roles': user_roles,  # Pass user roles to the template,
        'clients': clients,  # Pass clients to the template if user is superuser,
        'user_client': user.client.id if user.client else None,  # Pass the user's client ID
    }

    # Apply template layout enhancements (adds layout_path and other mappings)
    context = TemplateLayout().init(context)
    return render(request, 'edit_user.html', context)

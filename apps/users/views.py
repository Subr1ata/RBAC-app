from web_project import TemplateLayout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import CustomUser
from apps.authentication.models import Role

def view_users(request):
    template_name = "view_users.html"

    # Fetch all users
    # users = get_user_model().objects.all()
    # users = CustomUser.objects.all().prefetch_related('groups')
    # print("User is superuser:", request.user.is_superuser, CustomUser.objects.filter(client=request.user.client))

    # if(not request.user.client)

    if request.user.is_superuser:
        users = CustomUser.objects.all().prefetch_related('groups')
    else:
        users = CustomUser.objects.filter(client=request.user.client).prefetch_related('groups')
    # Initial context
    context = {
        "users": users,
    }

    # Apply template layout enhancements (adds layout_path and other mappings)
    context = TemplateLayout().init(context)

    return render(request, template_name, context)

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            if role:
                try:
                    custom_role = Role.objects.get(name=role)
                    user.roles.add(custom_role)
                except Role.DoesNotExist:
                    messages.error(request, f"Role '{role}' does not exist.")
            messages.success(request, "User created successfully!")
            return redirect('/users/list/')
    else:
        form = CustomUserCreationForm()

    roles = Role.objects.all()

    # Initial context
    context = {'form': form, 'roles': roles}

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
    User = get_user_model()  # Use the custom user model
    user = get_object_or_404(User, id=user_id)  # Fetch the user by ID

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
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
            print("Form is NOT valid ❌")
            print(form.errors.as_json())  # This will print all validation errors
    else:
        form = CustomUserEditForm(instance=user)

    roles = Role.objects.all()
    user_roles = user.roles.values_list('id', flat=True)  # Get the IDs of the user's roles

    # Initial context
    context = {
        'form': form,
        'roles': roles,
        'user': user,
        'user_roles': user_roles,  # Pass user roles to the template
    }

    # Apply template layout enhancements (adds layout_path and other mappings)
    context = TemplateLayout().init(context)
    return render(request, 'edit_user.html', context)

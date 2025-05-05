from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RoleForm, AssignPermissionsForm, ManagePermissionsForm
from .models import Role
from config.decorators import unauthenticated_user
from django.contrib.auth.models import Permission
from collections import defaultdict
from django.views.decorators.csrf import csrf_protect
from django.contrib.contenttypes.models import ContentType

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):
    def logout_view(request):
        logout(request)  # Log out the user
        messages.success(request, "You have been logged out successfully.")
        return redirect("auth-login-basic")  # Redirect to the login page

    @unauthenticated_user
    def loginPage(request):
        if request.method == 'POST':
            email = request.POST.get('email-username')  # Get email from the form
            password = request.POST.get('password')

            # Fetch the user model
            User = get_user_model()

            try:
                # Get the user by email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            # Authenticate using the username (from the user object) and password
            if user:
                user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('/')
            else:
                messages.error(request, 'Invalid email or password.')

        context = {}
        # Apply template layout enhancements (adds layout_path and other mappings)
        context = TemplateLayout().init(context)
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )
        return render(request, 'auth_login_basic.html', context)

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        if(self.request.path in ['/auth/login/']):
            context.update(
                {
                    "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                }
            )
        # Fetch all users
        users = get_user_model().objects.all()
        roles = Role.objects.all()
        context['roles'] = roles
        context['users'] = users
        return context

    def manage_roles(request):
        # Example form (replace with your actual form)
        if request.method == "POST":
            form = RoleForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Role created successfully!")
                return redirect("view-roles")
        else:
            form = RoleForm()

        roles = Role.objects.all()

        # Group permissions by app and model, excluding specific apps
        excluded_apps = ['social_django', 'sessions', 'contenttypes', 'auth', 'admin', 'Social_config', 'Social']
        permissions = Permission.objects.exclude(
            content_type__app_label='authentication',
            content_type__model='customuser'
        ).exclude(content_type__app_label__in=excluded_apps)

        # permissions = Permission.objects.exclude(content_type__app_label__in=excluded_apps)
        grouped_permissions = defaultdict(lambda: defaultdict(lambda: None))

        for perm in permissions:
            app_label = perm.content_type.app_label
            model = perm.content_type.model
            codename = perm.codename.split('_')[0]  # Extract action (e.g., 'add', 'change', etc.)
            grouped_permissions[(app_label, model)][codename] = perm

        # Convert grouped_permissions to a list for easier template rendering
        grouped_permissions_list = [
            {
                'app_model': app_model,
                'actions': [
                    {'action': action, 'permission': actions.get(action)}
                    for action in ['add', 'change', 'delete', 'view']
                ],
            }
            for app_model, actions in grouped_permissions.items()
        ]

        # Preprocess assigned permission IDs
        assigned_permission_ids = form.initial.get('permissions', [])
        if isinstance(assigned_permission_ids, list):
            assigned_permission_ids = [perm.id for perm in assigned_permission_ids]  # Ensure it's a list of IDs

        context = {
            'form': form,
            'grouped_permissions': grouped_permissions_list,
            'permission_actions': ['add', 'edit', 'delete', 'view'],
            "roles": roles,
            'assigned_permission_ids': assigned_permission_ids,  # Pass assigned permission IDs
        }

        context = TemplateLayout().init(context)

        return render(request, 'roles-permission/manage_roles.html', context)

    def delete_role(request, role_id):
        template_name = "roles-permission/manage_roles.html"
        # Get the specific role by ID or return a 404 if it doesn't exist
        role = get_object_or_404(Role, id=role_id)

        print('request.method ---> ' ,request.method)
        if request.method == "POST":
            # Delete the role
            role.delete()
            messages.success(request, f"Role '{role.name}' has been deleted successfully!")
            return redirect("view-roles")  # Redirect to the manage roles page

        # Initial context
        context = {
            "role": role,
        }

        # Apply template layout enhancements (adds layout_path and other mappings)
        context = TemplateLayout().init(context)

        return render(request, template_name, context)


    def view_permissions(request, role_id):
        template_name = "roles-permission/view_permissions.html"
        role = get_object_or_404(Role, id=role_id)

        if request.method == "POST":
            form = AssignPermissionsForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['user']
                selected_role = form.cleaned_data['role']

                # Optionally clear previous permissions
                user.user_permissions.clear()

                # Assign new permissions
                user.user_permissions.set(selected_role.permissions.all())

                messages.success(request, f"Permissions from role '{selected_role.name}' assigned to user '{user.username}'!")
                return redirect("manage_roles")
        else:
            form = AssignPermissionsForm()

        # Initial context
        context = {
            "role": role,
            "form": form
        }

        # Apply template layout enhancements (adds layout_path and other mappings)
        context = TemplateLayout().init(context)

        return render(request, template_name, context)

    def manage_permissions(request, role_id):
        template_name = "roles-permission/view_permissions.html"
        role = get_object_or_404(Role, id=role_id)

        if request.method == "POST":
            form = ManagePermissionsForm(request.POST, instance=role)
            if form.is_valid():
                form.save()
                messages.success(request, f"Permissions updated for role '{role.name}'!")
                return redirect("view-roles")
        else:
            form = ManagePermissionsForm(instance=role)

        # Group permissions by (app_label, model) with CRUD mapping
        grouped_permissions = defaultdict(lambda: {'create': None, 'read': None, 'update': None, 'delete': None})
        excluded_apps = ['social_django', 'sessions', 'contenttypes', 'auth', 'admin', 'Social_config', 'Social']
        all_permissions = Permission.objects.exclude(
            content_type__app_label='authentication',
            content_type__model='customuser'
        ).exclude(content_type__app_label__in=excluded_apps)

        for perm in all_permissions:
            app_label = perm.content_type.app_label
            model = perm.content_type.model
            codename = perm.codename

            if codename.startswith('add_'):
                grouped_permissions[(app_label, model)]['create'] = perm
            elif codename.startswith('view_'):
                grouped_permissions[(app_label, model)]['read'] = perm
            elif codename.startswith('change_'):
                grouped_permissions[(app_label, model)]['update'] = perm
            elif codename.startswith('delete_'):
                grouped_permissions[(app_label, model)]['delete'] = perm

        # Convert grouped_permissions to a list for easier template rendering
        grouped_permissions_list = [
            {
                'app_model': app_model,
                'permissions': [
                    {'label': label, 'permission': perms[label]}
                    for label in ['create', 'read', 'update', 'delete']
                ],
            }
            for app_model, perms in grouped_permissions.items()
        ]

        context = {
            "role": role,
            "form": form,
            "grouped_permissions": grouped_permissions_list,
            "permission_labels": ['create', 'read', 'update', 'delete'],
        }

        context = TemplateLayout().init(context)

        return render(request, template_name, context)

    @csrf_protect
    def list_create_delete_permissions(request):
        if request.method == "POST":
            if "perm_id" in request.POST:  # Handle deletion
                perm_id = request.POST.get("perm_id")
                try:
                    perm = Permission.objects.get(id=perm_id)
                    perm.delete()
                    messages.success(request, f"Permission '{perm.name}' deleted successfully.")
                except Permission.DoesNotExist:
                    messages.error(request, "Permission not found.")
                return redirect("list-permissions")

            elif "codename" in request.POST:  # Handle creation
                name = request.POST.get("name")
                codename = request.POST.get("codename")
                app_label = request.POST.get("app_label")
                model = request.POST.get("model")

                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    if Permission.objects.filter(codename=codename).exists():
                        messages.warning(request, f"A permission with codename '{codename}' already exists.")
                    else:
                        Permission.objects.create(
                            codename=codename,
                            name=name,
                            content_type=content_type
                        )
                        messages.success(request, f"Permission '{name}' created successfully.")
                except ContentType.DoesNotExist:
                    messages.error(request, "Invalid app label or model name.")

                return redirect("list-permissions")

        excluded_apps = ['social_django', 'sessions', 'contenttypes', 'auth', 'admin', 'Social_config', 'Social']
        permissions = Permission.objects.exclude(
            content_type__app_label__in=excluded_apps
        ).order_by('content_type__app_label', 'content_type__model', 'codename')

        content_types = ContentType.objects.exclude(app_label__in=excluded_apps)

        context = {
            "permissions": permissions,
            "content_types": content_types,
        }

        context = TemplateLayout().init(context)

        return render(request, "permissions/list_permissions.html", context)

from django.urls import path
from .views import AuthView

urlpatterns = [
    path(
        "auth/login/",
        AuthView.loginPage,
        # AuthView.as_view(template_name="auth_login_basic.html"),
        name="auth-login-basic",
    ),

    path(
        "auth/register/",
        AuthView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    path(
        "auth/forgot_password/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password-basic",
    ),
    path("auth/logout/", AuthView.logout_view, name="auth-logout"),  # Add this line for logout

    path("auth/view-permissions/<int:role_id>/", AuthView.manage_permissions, name="view-permissions"),
    path("auth/view-roles/", AuthView.as_view(template_name="roles-permission/view_roles.html"), name="view-roles"),
    path("auth/create-role/", AuthView.as_view(), name="create-role"),
    path("auth/manage-roles/", AuthView.manage_roles, name="manage-roles"),
    path("auth/delete-role/<int:role_id>/", AuthView.delete_role, name="delete-role"),
    path("auth/edit-role/<int:role_id>/", AuthView.manage_permissions, name="edit-role"),  # Add this for editing roles
]

from .views import view_users, create_user, edit_user, delete_user
from django.urls import path

urlpatterns = [
    path("users/list/", view_users, name="view_users"),
    path("users/create/", create_user, name="create_user"),
    path('edit/<int:user_id>/', edit_user, name='edit_user'),
    path("delete/<int:user_id>/", delete_user, name="delete_user"),  # <-- Add this line
]

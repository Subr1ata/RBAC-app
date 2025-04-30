from django.urls import path
from .views import register_client

# app_name = 'social_config'

urlpatterns = [
    path('client/register/', register_client, name='register_client'),
]

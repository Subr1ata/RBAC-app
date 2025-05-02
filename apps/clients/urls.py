from django.urls import path
from .views import register_client,registered_clients, add_client_ajax

# app_name = 'social_config'

urlpatterns = [
    path('client/register/', registered_clients, name='register_client'),
    path('client/add-ajax/', add_client_ajax, name='add_client_ajax'),
]

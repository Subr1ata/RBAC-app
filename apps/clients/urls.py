from django.urls import path
from .views import registered_clients, add_client_ajax, delete_client_ajax, update_client_ajax, get_client_ajax

# app_name = 'social_config'

urlpatterns = [
    path('client/register/', registered_clients, name='register_client'),
    path('client/add-ajax/', add_client_ajax, name='add_client_ajax'),
    path('client/delete/<int:client_id>/', delete_client_ajax, name='delete_client_ajax'),
    path('client/update/<int:client_id>/', update_client_ajax, name='update_client_ajax'),
    path('client/<int:client_id>/', get_client_ajax, name='get_client_ajax'),  # New endpoint
]

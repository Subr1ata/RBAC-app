from django.urls import path
from .views import DashboardsView



urlpatterns = [
    path(
        "",
        DashboardsView.home,
        name="index",
    )
]

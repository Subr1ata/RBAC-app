from django.urls import path
from apps.marketing.views.facebook import FacebookManageView

# app_name = "marketing"

urlpatterns = [
    path('marketing/facebook/manage/', FacebookManageView.as_view(), name='facebook_manage'),
    path('marketing/facebook/select-page/<str:page_id>/<str:access_token>/', FacebookManageView.select_facebook_page, name='facebook_select_page'),
]

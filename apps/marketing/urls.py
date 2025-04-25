from django.urls import path
from apps.marketing.views.facebook import FacebookManageView

# app_name = "marketing"

urlpatterns = [
    path('facebook/manage/', FacebookManageView.as_view(), name='facebook_manage'),
    path('facebook/select-page/<str:page_id>/<str:access_token>/', FacebookManageView.select_facebook_page, name='facebook_select_page'),
]

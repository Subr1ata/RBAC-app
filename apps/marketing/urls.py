from django.urls import path
from apps.marketing.views.facebook import FacebookManageView

# app_name = "marketing"

urlpatterns = [
    path('marketing/facebook/manage/', FacebookManageView.as_view(), name='facebook_manage'),
    path('marketing/facebook/select-page/<str:page_id>/<str:access_token>/', FacebookManageView.select_facebook_page, name='facebook_select_page'),
    path('marketing/facebook/create-post/', FacebookManageView.create_post,name='facebook_create_post'),
    path('marketing/facebook/sync-feeds/<str:page_id>/<str:access_token>/', FacebookManageView.sync_feeds, name='sync_feeds')
]

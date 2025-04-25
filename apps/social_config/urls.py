from django.urls import path
from .views import SocialView
# from .views_misc import MiscPagesView

urlpatterns = [
    path(
        "account_settings/social_media_settings/",
        SocialView.as_view(template_name="social_media_settings.html"),
        name="social-media-settings",
    ),
    path("facebook/callback/", SocialView.facebook_callback, name="facebook_callback"),
]

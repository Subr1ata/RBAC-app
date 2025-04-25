# apps/social/backends.py

from social_core.backends.facebook import FacebookOAuth2
from apps.social_config.models import SocialMediaIntegration

class DynamicFacebookOAuth2(FacebookOAuth2):
    def get_key_and_secret(self):
        fb = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if fb and fb.api_key and fb.api_secret:
            return fb.api_key, fb.api_secret
        return super().get_key_and_secret()

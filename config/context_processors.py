from django.conf import settings
from apps.social_config.models import SocialMediaIntegration

def my_setting(request):
    return {'MY_SETTING': settings}


# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}

# def facebook_credentials(request):
#     try:
#         fb = SocialMediaIntegration.objects.filter(platform="facebook").first()
#         print("SocialMediaIntegration 15: ", SocialMediaIntegration.objects.count())
#         return {
#             "SOCIAL_AUTH_FACEBOOK_KEY": fb.api_key if fb else "",
#             "SOCIAL_AUTH_FACEBOOK_SECRET": fb.api_secret if fb else ""
#         }
#     except Exception:
#         return {
#             "SOCIAL_AUTH_FACEBOOK_KEY": "",
#             "SOCIAL_AUTH_FACEBOOK_SECRET": ""
#         }

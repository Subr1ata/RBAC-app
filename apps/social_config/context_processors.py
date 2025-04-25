from apps.social_config.models import SocialMediaIntegration

def social_configs(request):
    try:
        fb = SocialMediaIntegration.objects.filter(platform="facebook").first()
        insta = SocialMediaIntegration.objects.filter(platform="instagram").first()

        is_facebook_enabled = fb.is_enabled if fb else False
        is_instagram_enabled = insta.is_enabled if insta else False

        return {
            "show_marketing_menu": is_facebook_enabled or is_instagram_enabled,  # True if either is enabled
            "is_facebook_enabled": is_facebook_enabled,
            "is_instagram_enabled": is_instagram_enabled,
            "SOCIAL_AUTH_FACEBOOK_KEY": fb.api_key if fb else "",
            "SOCIAL_AUTH_FACEBOOK_SECRET": fb.api_secret if fb else ""
        }
    except Exception:
        return {
            "show_marketing_menu": False,
            "is_facebook_enabled": False,
            "is_instagram_enabled": False,
            "SOCIAL_AUTH_FACEBOOK_KEY": "",
            "SOCIAL_AUTH_FACEBOOK_SECRET": ""
        }

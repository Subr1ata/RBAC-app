from django.shortcuts import render, redirect
from .models import SocialMediaIntegration
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.utils.safestring import mark_safe
import json
from django.core.serializers.json import DjangoJSONEncoder
from config.context_processors import facebook_credentials

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class SocialView(TemplateView):
    @login_required
    def facebook_callback(request):
        try:
            # Get the user's social auth object for Facebook
            user_social_auth = request.user.social_auth.get(provider='facebook')
            access_token = user_social_auth.extra_data['access_token']

            # Save the access token to the database
            SocialMediaIntegration.objects.update_or_create(
                platform="facebook",
                defaults={"access_token": access_token, "is_enabled": True},
            )

            # Save the access token to the database or use it as needed
            # messages.success(request, f"Facebook Access Token: {access_token}")
            messages.success(request, "Facebook Access Token saved successfully!")

        except UserSocialAuth.DoesNotExist:
            messages.error(request, "Facebook authentication failed.")
            # messages.error(request, "Facebook authentication failed.")

        return redirect('/account_settings/social_media_settings/')

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        integrations_qs = SocialMediaIntegration.objects.all()

        integrations = list(integrations_qs.values())  # ✅ Convert to list of dicts
        integrations_json = json.dumps(integrations, cls=DjangoJSONEncoder)

        context['integrations'] = SocialMediaIntegration.objects.all()
        context['integrations_json'] = integrations_json
        return context

    # def get(self, request):
    #     integrations_qs = SocialMediaIntegration.objects.all()

    #     integrations = list(integrations_qs.values())  # ✅ Convert to list of dicts
    #     integrations_json = mark_safe(json.dumps(integrations))

    #     return render(request, 'social_media_settings.html', {
    #         'integrations': integrations_qs,
    #         'integrations_json': integrations_json,
    #     })

    # Handle POST requests
    def post(self, request, *args, **kwargs):
        # Capture form data
        platform = request.POST.get("platform")
        is_enabled = request.POST.get("is_enabled") == "on"
        api_key = request.POST.get("api_key")
        api_secret = request.POST.get("api_secret")

        # Save or update the integration in the database
        SocialMediaIntegration.objects.update_or_create(
            platform=platform,
            defaults={
                "is_enabled": is_enabled,
                "api_key": api_key,
                "api_secret": api_secret,
            },
        )

        # Add a success message
        messages.success(request, "Social media integration saved successfully!")

        # Redirect to the same page after saving
        return redirect("/account_settings/social_media_settings/")

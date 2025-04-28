from django.shortcuts import render, redirect
from .models import SocialMediaIntegration
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class SocialView(TemplateView):
    @login_required
    def facebook_callback(request):
        try:
            print('facebook_callback called')
            # Get the user's social auth object for Facebook
            user_social_auth = request.user.social_auth.get(provider='facebook')
            access_token = user_social_auth.extra_data['access_token']

            user_info_url = f"https://graph.facebook.com/me?access_token={access_token}"
            user_profile_img_url = f"https://graph.facebook.com/me/picture?type=large&redirect=false&access_token={access_token}"

            user_info_response = requests.get(user_info_url)
            user_info_response.raise_for_status()

            user_profile_img_response = requests.get(user_profile_img_url)
            user_profile_img_response.raise_for_status()

            user_info = user_info_response.json()
            user_id = user_info.get("id")

            user_profile_img = user_profile_img_response.json().get("data", {})
            profile_img_url = user_profile_img.get('url')

            pages_url = f"https://graph.facebook.com/v22.0/{user_id}/accounts?access_token={access_token}"
            response = requests.get(pages_url)
            response.raise_for_status()
            pages_data = response.json().get("data", [])

            if not pages_data:
                messages.error(request, "No pages found for this Facebook account.")
                return redirect('/account_settings/social_media_settings/')

            for page in pages_data:
                page_id = page.get('id')
                page_access_token = page.get('access_token')
                page_image_url = f"https://graph.facebook.com/{page_id}/picture?type=large&redirect=false&access_token={page_access_token}"
                feeds_url = f"https://graph.facebook.com/{page_id}/feed?fields=message,created_time,full_picture,attachments{{media}}&access_token={page_access_token}"

                # Fetch page image
                page_image_res = requests.get(page_image_url)
                page_image_res.raise_for_status()
                page_image_data = page_image_res.json().get("data", {})

                # Fetch feeds
                feeds_res = requests.get(feeds_url)
                feeds_res.raise_for_status()
                feeds = feeds_res.json().get("data", [])

                page['img'] = page_image_data.get('url')
                page['feeds'] = feeds

            user_info['img'] = profile_img_url
            user_info['access_token'] = access_token

            social_user_details = {
                "user_info": user_info,
                "all_pages": pages_data,
            }

            # Save the access token and social_user_details to the database
            SocialMediaIntegration.objects.update_or_create(
                platform="facebook",
                defaults={
                    "is_enabled": True,
                    "social_user_details": social_user_details,  # Save as JSON
                },
            )

            messages.success(request, "Facebook user details saved successfully!")

        except UserSocialAuth.DoesNotExist:
            messages.error(request, "Facebook authentication failed.")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error fetching data from Facebook: {e}")

        return redirect('/account_settings/social_media_settings/')

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        facebook_integration, created = SocialMediaIntegration.objects.get_or_create(platform="facebook")
        integrations_qs = SocialMediaIntegration.objects.all()

        # if facebook_integration and facebook_integration.social_user_details:
        #     context['social_user_details'] = facebook_integration.social_user_details
        # else:
        #     context['social_user_details'] = {}

        # return context

        integrations = list(integrations_qs.values())  # ✅ Convert to list of dicts
        integrations_json = json.dumps(integrations, cls=DjangoJSONEncoder)

        # Ensure social_user_details is a valid dictionary
        social_user_details = facebook_integration.social_user_details or {}
        user_info = social_user_details.get("user_info", {})
        # all_pages = social_user_details.get("all_pages", [])

        # Extract the access token
        access_token = user_info.get("access_token", "")

        # Debugging: Print the extracted access token
        print("Access Token:", access_token)

         # Pass data to the template
        context["social_user_details"] = social_user_details
        context["access_token"] = access_token
        context['integrations'] = SocialMediaIntegration.objects.all()
        context['integrations_json'] = integrations_json
        context['api_key'] = facebook_integration.api_key
        context['api_secret'] = facebook_integration.api_secret
        return context

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

    def social_media_settings(request):
        # Retrieve the Facebook integration from the database
        facebook_integration, created = SocialMediaIntegration.objects.get_or_create(platform="facebook")

        if request.method == "POST":
            # platform = request.POST.get("platform")
            # is_enabled = request.POST.get("is_enabled") == "on"
            # Save API Key and Secret
            api_key = request.POST.get("api_key")
            api_secret = request.POST.get("api_secret")

            if api_key and api_secret:
                facebook_integration.api_key = api_key
                facebook_integration.api_secret = api_secret
                facebook_integration.save()
                messages.success(request, "API Key and Secret saved successfully.")
            else:
                messages.error(request, "Both API Key and API Secret are required.")

            return redirect("social_media_settings")

        # Pass data to the template
        context = {
            "api_key": facebook_integration.api_key,
            "api_secret": facebook_integration.api_secret,
            "access_token": facebook_integration.access_token,
        }

        # context = TemplateLayout().init(context)

        return render(request, "social_media_settings.html", context)

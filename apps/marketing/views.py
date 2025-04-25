from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from apps.social_config.models import SocialMediaIntegration
import requests
import datetime
from web_project import TemplateLayout
from django.http import JsonResponse

class FacebookManageView(TemplateView):
    template_name = "facebook/manage.html"

    def facebook_marketing(self):
        # Fetch Facebook integration details
        facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if not facebook_integration or not facebook_integration.page_access_token:
            messages.error(self.request, "Please connect to Facebook and select a page first.")
            return None

        # Fetch Facebook page feeds
        page_id = facebook_integration.page_id
        page_access_token = facebook_integration.page_access_token
        feeds_url = f"https://graph.facebook.com/v22.0/{page_id}/feed?access_token={page_access_token}"
        response = requests.get(feeds_url)
        feeds = response.json().get("data", [])

        context = {
            "page_name": facebook_integration.page_id,
            "page_access_token": facebook_integration.page_access_token,
            "feeds": feeds,
            "page_id": page_id,
        }
        context = TemplateLayout().init(context)

        return context

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch Facebook integration details
        facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if not facebook_integration or not facebook_integration.access_token:
            messages.error(self.request, "Please connect to Facebook and select a page first.")
            return context

        # Fetch Facebook page feeds and profile picture
        page_access_token = facebook_integration.access_token

        user_info_url = f"https://graph.facebook.com/me?access_token={page_access_token}"
        user_profile_pic_url = f"https://graph.facebook.com/me/picture?type=large&redirect=false&access_token={page_access_token}"

        try:
            # Fetch user info
            user_info_res = requests.get(user_info_url)
            user_info_res.raise_for_status()
            user_info = user_info_res.json()  # Extract user info
            user_id = user_info.get("id")  # Extract the user ID
            print('user_id ---> ', user_id)

            # Fetch profile picture
            profile_pic_img_res = requests.get(user_profile_pic_url)
            profile_pic_img_res.raise_for_status()
            profile_pic_img = profile_pic_img_res.json().get("data", {})

            # Fetch Facebook accounts
            fb_account_url = f"https://graph.facebook.com/v22.0/{user_id}/accounts?access_token={page_access_token}"
            fb_account_res = requests.get(fb_account_url)
            fb_account_res.raise_for_status()
            fb_account = fb_account_res.json().get("data", [])

            # Iterate through accounts and fetch page images
            for account in fb_account:
                page_id = account.get("id")
                page_access_token = account.get("access_token")
                page_image_url = f"https://graph.facebook.com/{page_id}/picture?type=large&redirect=false&access_token={page_access_token}"

                # Fetch page image
                page_image_res = requests.get(page_image_url)
                page_image_res.raise_for_status()
                page_image_data = page_image_res.json().get("data", {})

                # Add the image URL to the account object
                account["page_image_url"] = page_image_data.get("url")
                print(f"Page ID: {page_id}, Image URL: {account['page_image_url']}")

            # Fetch feeds using the user ID
            feeds_url = f"https://graph.facebook.com/v22.0/{user_id}/feed?access_token={page_access_token}"
            response = requests.get(feeds_url)
            response.raise_for_status()
            feeds = response.json().get("data", [])
        except requests.exceptions.RequestException as e:
            print('Error fetching data from Facebook API:', e)
            profile_pic_img = {}
            feeds = []
            user_info = {}
            fb_account = []

        context["feeds"] = feeds
        context["page_name"] = facebook_integration.page_id
        context["page_access_token"] = facebook_integration.page_access_token
        context["fb_user"] = {
            "picture": profile_pic_img.get("url", None),
            "user_info": user_info,
            "account": fb_account
        }
        return context

    def post(self, request, *args, **kwargs):
        # Handle post creation, scheduling, or queueing
        facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if not facebook_integration or not facebook_integration.page_access_token:
            messages.error(request, "Please connect to Facebook and select a page first.")
            return redirect("marketing:facebook_manage")

        page_id = facebook_integration.page_id
        page_access_token = facebook_integration.page_access_token

        # Get form data
        message = request.POST.get("message")
        schedule_time = request.POST.get("schedule_time")  # Optional for scheduling

        if not message:
            messages.error(request, "Message content is required.")
            return redirect("marketing:facebook_manage")

        # Prepare API request
        post_url = f"https://graph.facebook.com/v22.0/{page_id}/feed"
        payload = {"message": message, "access_token": page_access_token}

        # Add scheduling if provided
        if schedule_time:
            schedule_time_unix = int(datetime.datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S").timestamp())
            payload["published"] = False
            payload["scheduled_publish_time"] = schedule_time_unix

        # Send the post request
        response = requests.post(post_url, data=payload)
        if response.status_code == 200:
            messages.success(request, "Post created successfully.")
        else:
            messages.error(request, f"Failed to create post: {response.json().get('error', {}).get('message')}")

        return redirect("marketing:facebook_manage")

    def select_facebook_page(request, page_id, access_token):
        facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if not facebook_integration or not facebook_integration.access_token:
            return JsonResponse({"error": "Please connect to Facebook first."}, status=400)

        # access_token = facebook_integration.access_token
        feeds_url = f"https://graph.facebook.com/{page_id}/feed?fields=message,created_time&access_token={access_token}"
        page_details_url = f"https://graph.facebook.com/{page_id}?fields=name,picture&access_token={access_token}"

        try:
            # Fetch page details
            page_details_res = requests.get(page_details_url)
            page_details_res.raise_for_status()
            page_details = page_details_res.json()

            # Fetch feeds
            feeds_res = requests.get(feeds_url)
            feeds_res.raise_for_status()
            feeds = feeds_res.json().get("data", [])

            # Save selected page to the database
            facebook_integration.page_id = page_id
            # facebook_integration.page_name = page_details.get("name")
            # facebook_integration.page_image_url = page_details.get("picture", {}).get("data", {}).get("url")
            facebook_integration.save()

            # Generate HTML for the feed preview
            feed_html = ""
            for feed in feeds:
                feed_html += f"<div class='card card-body mb-2'><p>{feed.get('message', 'No message')}</p><small>{feed.get('created_time')}</small></div>"

            return JsonResponse({
                "feed_html": feed_html,
                "selected_page": {
                    "name": page_details.get("name"),
                    "image_url": page_details.get("picture", {}).get("data", {}).get("url"),
                }
            }, status=200)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

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

        # Fetch Facebook integration details from the database
        facebook_integration = SocialMediaIntegration.objects.filter(platform="facebook").first()
        if not facebook_integration:
            messages.error(self.request, "Please connect to Facebook first.")
            return context

        # Ensure social_user_details is a valid dictionary
        social_user_details = facebook_integration.social_user_details or {}
        user_info = social_user_details.get("user_info", {})
        all_pages = social_user_details.get("all_pages", [])
        page_id = facebook_integration.page_id

        # Extract the page access token from the first page (if available)
        for account in all_pages:
            account["page_access_token"] = account.get("access_token")

        # Find the selected page
        selected_page = next((page for page in all_pages if page.get("id") == page_id), None)

        # Pass data from the database to the template
        # Pass the selected page details to the template
        context["selected_page"] = selected_page
        context["fb_user"] = {
            "name": user_info.get("name"),
            "id": user_info.get("id"),
            "img": user_info.get("img"),
            "access_token": user_info.get("access_token"),
            "all_pages": all_pages,
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

        if not facebook_integration or not facebook_integration.social_user_details:
            return JsonResponse({"error": "Please connect to Facebook first."}, status=400)

        # Get all pages from social_user_details
        social_user_details = facebook_integration.social_user_details or {}
        all_pages = social_user_details.get("all_pages", [])
        selected_page = next((page for page in all_pages if page.get("id") == page_id), None)

        if not selected_page:
            return JsonResponse({"error": "Selected page not found."}, status=400)

        feeds_url = f"https://graph.facebook.com/{page_id}/feed?fields=message,created_time&access_token={access_token}"

        try:

            # Fetch feeds
            feeds_res = requests.get(feeds_url)
            feeds_res.raise_for_status()
            feeds = feeds_res.json().get("data", [])

            # Save selected page to the database
            facebook_integration.page_id = page_id
            facebook_integration.page_access_token = access_token

            # Update social_user_details with feeds
            selected_page["feeds"] = feeds
            social_user_details["all_pages"] = all_pages
            facebook_integration.social_user_details = social_user_details
            facebook_integration.save()

            # Generate HTML for the feed preview
            feed_html = ""
            for feed in feeds:
                feed_html += f"<div class='card card-body mb-2'><p>{feed.get('message', 'No message')}</p><small>{feed.get('created_time')}</small></div>"

            return JsonResponse({
                "feed_html": feed_html,
                "selected_page": {
                    "name": selected_page.get("name"),
                    "image_url": selected_page.get("img"),
                }
            }, status=200)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)

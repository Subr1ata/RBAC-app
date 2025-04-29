from celery import shared_task
import requests

# @shared_task
# def sharedtask():
#     return

@shared_task(bind=True, max_retries=3)
def schedule_facebook_post(self, page_id, page_access_token, message, schedule_time):
    try:
        post_url = f"https://graph.facebook.com/v16.0/{page_id}/feed"
        payload = {
            "message": message,
            "access_token": page_access_token,
            "published": False,
            "scheduled_publish_time": schedule_time,
        }
        response = requests.post(post_url, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        raise self.retry(exc=exc, countdown=60)  # Retry after 60 seconds

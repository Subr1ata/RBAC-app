from django.db import models
from apps.clients.models import Client

class SocialMediaIntegration(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="social_integrations")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    is_enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    page_id = models.CharField(max_length=255, blank=True, null=True)  # Facebook Page ID
    page_access_token = models.TextField(blank=True, null=True)  # Page Access Token
    social_user_details = models.JSONField(blank=True, null=True)  # Store user details as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform} - {self.client.name}"

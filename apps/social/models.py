from django.db import models

class SocialMediaIntegration(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    is_enabled = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)  # Ensure this field exists
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.platform

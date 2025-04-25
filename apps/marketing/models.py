from django.db import models

# Create your models here.
class Marketing(models.Model):
    name = models.CharField(max_length=255)  # Name of the marketing campaign or feature
    description = models.TextField(blank=True, null=True)  # Optional description
    is_active = models.BooleanField(default=True)  # Whether the marketing feature is active
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    class Meta:
        permissions = [
            # ("add_marketing", "Can add marketing"),
            # ("view_marketing", "Can view marketing"),
            # ("delete_marketing", "Can delete marketing"),
            ("edit_marketing", "Can edit marketing"),
        ]

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    api_key = models.CharField(max_length=255, unique=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)  # Optional business name
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    address = models.TextField(blank=True, null=True)  # Optional address
    unique_store_code = models.CharField(max_length=100, unique=True, null=True, blank=True,)  # Unique store code

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

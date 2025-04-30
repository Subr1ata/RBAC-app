from django import forms
from .models import Client

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'business_name', 'phone_number', 'address', 'unique_store_code']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),  # Optional: Make the address field a textarea
        }

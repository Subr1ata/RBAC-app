from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from apps.authentication.models import Role
from django.contrib.auth import get_user_model
from apps.clients.models import Client
import re

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=False,
        label="Client",
        help_text="Select a client (only for superadmins)."
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'client')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("This field is required.")
        if not re.match(r'^[\w.@+-]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
        return username

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Assign the user to self.user
        super().__init__(*args, **kwargs)
        if not self.user or not self.user.is_superuser:
            self.fields.pop('client')  # Remove the client field for non-superadmins

    def save(self, commit=True):
        user = super().save(commit=False)

        print('user -> ', self.user)
        if self.user and self.user.is_superuser:
            user.is_staff = True  # Only set is_staff to True if the logged-in user is a superadmin
        else:
            user.is_staff = False  # Set is_staff to False for non-superadmins
        # user.is_staff = True  # Set is_staff to 1
        user.is_superuser = False  # Set is_superuser to 0

        # Save the client field if it exists in the form data

        client = self.cleaned_data.get('client')
        print('save client -> ', client)
        if client:
            user.client = client

        if commit:
            user.save()
        return user

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )


class CustomUserEditForm(forms.ModelForm):
    # roles = forms.ModelMultipleChoiceField(
    #     queryset=Role.objects.all(),
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple
    # )

    # class Meta:
    #     model = User
    #     fields = ('username', 'email')
    #     widgets = {
    #         'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
    #     }

    # def __init__(self, *args, **kwargs):
    #     self.instance = kwargs.get('instance', None)
    #     super().__init__(*args, **kwargs)

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     qs = User.objects.filter(username=username)
    #     if self.instance:
    #         qs = qs.exclude(pk=self.instance.pk)
    #     if qs.exists():
    #         raise forms.ValidationError("A user with that username already exists.")
    #     return username
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=False,
        label="Client",
        help_text="Select a client (only for superadmins)."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'client')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass the current user to the form
        super().__init__(*args, **kwargs)

        # Only show the client field to superusers
        if not user or not user.is_superuser:
            self.fields.pop('client')  # Remove the client field for non-superadmins

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save the client field if it exists in the form data
        client = self.cleaned_data.get('client')
        if client:
            user.client = client

        if commit:
            user.save()
        return user

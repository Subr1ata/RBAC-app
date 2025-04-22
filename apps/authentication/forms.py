from django import forms
from .models import Role
from apps.users.models import CustomUser

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter role name'
            }),
            'permissions': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }

class AssignPermissionsForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Select User")
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Select Role")

class ManagePermissionsForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'permissions']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sure permissions are pre-filled based on the role instance
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

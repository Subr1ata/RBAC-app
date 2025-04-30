from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from apps.authentication.models import Role
from apps.clients.models import Client

# Create your models here.
class CustomUser(AbstractUser):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Custom related_name to avoid conflict
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    def get_all_permissions(self):
        perms = set()
        for role in self.roles.all():
            perms.update(role.permissions.all())
        return perms

    def has_perm(self, perm, obj=None):
        # return perm in [p.codename for p in self.get_all_permissions()] or super().has_perm(perm)
        """
        Custom has_perm implementation that checks role permissions too.
        Accepts 'app_label.codename' format as Django uses.
        """
        if super().has_perm(perm, obj):
            return True

        try:
            app_label, codename = perm.split('.')
        except ValueError:
            return False  # Incorrect format

        return any(
            p.codename == codename and p.content_type.app_label == app_label
            for p in self.get_all_permissions()
        )

    @property
    def role_names(self):
        return ", ".join(role.name for role in self.roles.all())

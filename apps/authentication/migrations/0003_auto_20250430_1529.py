from django.db import migrations

def create_client_roles(apps, schema_editor):
    # Get the Role model
    Role = apps.get_model('authentication', 'Role')

    # Define the roles
    roles = [
        {"name": "Client Admin"},
        {"name": "Client Subuser"},
    ]

    # Create the roles
    for role_data in roles:
        Role.objects.get_or_create(name=role_data["name"])

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_delete_customuser'),  # Ensure this matches the last migration in the authentication app
    ]

    operations = [
        migrations.RunPython(create_client_roles),
    ]

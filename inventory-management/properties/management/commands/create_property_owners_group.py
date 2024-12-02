from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from properties.models import Accommodation

class Command(BaseCommand):
    help = 'Create Property Owners group with limited permissions'

    def handle(self, *args, **kwargs):
        # Check if the group already exists
        group, created = Group.objects.get_or_create(name='Property Owners')

        if created:
            self.stdout.write(self.style.SUCCESS('Property Owners group created.'))
        else:
            self.stdout.write(self.style.WARNING('Property Owners group already exists.'))

        # Get content type for the Accommodation model
        content_type = ContentType.objects.get_for_model(Accommodation)

        # Define the permissions to assign
        permissions = [
            Permission.objects.get(codename='add_accommodation', content_type=content_type),
            Permission.objects.get(codename='change_accommodation', content_type=content_type),
            Permission.objects.get(codename='view_accommodation', content_type=content_type),
        ]

        # Assign permissions to the group
        for permission in permissions:
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Permissions assigned to Property Owners group.'))

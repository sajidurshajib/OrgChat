from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        # Add custom prompts for 'role' and 'phone_number'
        phone_number = options.get('phone_number')
        role = options.get('role')

        # Ensure required fields are provided
        if not phone_number:
            raise CommandError(_("Phone number is required"))

        if not role:
            raise CommandError(_("Role is required"))

        # Call the original createsuperuser command to handle the rest
        super().handle(*args, **options)

    def add_arguments(self, parser):
        # Add custom arguments for 'phone_number' and 'role'
        super().add_arguments(parser)

        parser.add_argument(
            '--phone_number',
            default=None,
            help='Phone number of the user'
        )
        parser.add_argument(
            '--role',
            default='admin',
            help='Role of the user (default: admin)'
        )

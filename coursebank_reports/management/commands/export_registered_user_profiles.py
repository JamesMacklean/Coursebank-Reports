from django.core.management.base import BaseCommand, CommandError

from coursebank_reports.handlers import export_registered_user_profiles

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--email',
            type=str,
            help='set email to send report to',
        )

    def handle(self, *args, **options):
        email_address = options.get('email', None)

        try:
            export_registered_user_profiles(email_address=email_address)
        except Exception as e:
            raise CommandError("{}".format(str(e)))

        self.stdout.write(self.style.SUCCESS("Successfully exported registered user profiles."))

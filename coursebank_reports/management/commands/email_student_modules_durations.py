from django.core.management.base import BaseCommand

from coursebank_reports.handlers import email_student_modules_durations

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--course',
            type=str,
            help='set course ID',
        )

    def handle(self, *args, **options):
        course_id = options.get('course', None)

        if not course_id:
            raise CommandError("Arguments course_id -c --course is required.")

        try:
            email_student_modules_durations(course_id)
        except Exception as e:
            raise CommandError("{}".format(str(e)))

        self.stdout.write(self.style.SUCCESS("Successfully emailed student modules durations."))

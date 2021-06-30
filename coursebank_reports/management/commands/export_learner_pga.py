import csv
import os
from pprint import pformat

import logging
log = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError

from coursebank_reports.utils import export_learner_pga


class Command(BaseCommand):
    help = 'Exports learner PGAs.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--email',
            type=str,
            help='set email to send to',
        )
        parser.add_argument(
            '-c',
            '--course',
            type=str,
            help='set filter for course_id',
        )

    def handle(self, *args, **options):
        course_id = options.get('course', None)
        email_address = options.get('email', None)

        try:
            export_learner_pga(course_id, email_address=email_address)
        except Exception as e:
            raise CommandError("Error in exporting learner pga: {}".format(str(e)))
        else:
            self.stdout.write(self.style.SUCCESS("Successfully exported learner pga."))

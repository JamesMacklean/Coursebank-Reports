import csv
from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--start',
            type=str,
            help='set start date',
        )
        parser.add_argument(
            '-e',
            '--end',
            type=str,
            help='set end date',
        )
        parser.add_argument(
            '-a',
            '--address',
            type=str,
            help='set email address if you want to email report',
        )

    def handle(self, *args, **options):
        start_date_str = options.get('start', None)
        end_date_str = options.get('end', None)
        address = options.get('address', None)

        if start_date_str is None:
            start_date_str = "2018-09-13" # date of first ever user date_joined
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        if end_date_str is not None:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        else:
            end_date = timezone.now().date() + timedelta(days=1)
            end_date_str = end_date.strftime('%Y-%m-%d')

        users = User.objects.filter(date_joined__gte=start_date).filter(date_joined__lte=end_date)

        self.stdout.write(self.style.HTTP_INFO("User count from {} to {}: {}".format(start_date_str, end_date_str, users.count())))

        start_text = "From: {}".format(start_date_str)
        end_text = "To: {}".format(end_date_str)

        tnow = datetime.now().strftime('%Y-%m-%d')

        file_name = '/home/ubuntu/tempfiles/coursebank-users-count-report-{}.csv'.format(tnow)
        with open(file_name, mode='w') as apps_file:
            writer = csv.writer(apps_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([start_text, end_text,])
            writer.writerow(['Count:', users.count(),])
            writer.writerow(['Username', 'Email',])
            for user in users:
                writer.writerow([user.username, user.email])

        if address is not None:
            email = EmailMessage(
            'Coursebank User Count Report - {}'.format(tnow),
            'Attached file of Coursebank User Count Report',
            'no-reply-user-count-report@coursebank.ph',
            [address,],
            )
            email.attach_file(file_name)
            email.send()


        msg = 'Successfully generated user count report.'
        log.info(msg)
        self.stdout.write(self.style.SUCCESS(msg))

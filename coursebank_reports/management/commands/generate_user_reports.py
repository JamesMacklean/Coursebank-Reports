from django.core.management.base import BaseCommand

from coursebank_reports.handlers import UserCountReportGenerator

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def handle(self, *args, **kwargs):
        gtr = UserCountReportGenerator()

        registration_report = gtr.generate_registration_count_report()
        registrations_today_report = gtr.generate_registration_today_count_report()
        user_report = gtr.generate_user_count_report()
        active_report = gtr.generate_active_user_count_report()
        active_today_report = gtr.generate_active_users_today_count_report()
        inactive_report = gtr.generate_inactive_user_count_report()
        non_staff_report = gtr.generate_non_staff_user_count_report()
        staff_report = gtr.generate_staff_user_count_report()

        msg = 'Successfully generated user reports.'
        log.info(msg)

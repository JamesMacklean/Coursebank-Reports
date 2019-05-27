from django.core.management.base import BaseCommand

from coursebank_reports.generators import CourseCountReportGenerator

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    This management command generates reports.
    """
    help = 'This management command generates reports.'

    def handle(self, *args, **kwargs):
        gtr = CourseCountReportGenerator()

        course_report = gtr.generate_course_overview_count_report()
        verified_course_report = gtr.generate_verified_course_count_report()
        enrollment_report = gtr.generate_enrollment_count_report()
        enrollments_today_report = gtr.generate_enrollment_count_today_report()
        verified_enrollment_report = gtr.generate_verified_enrollment_count_report()
        verified_enrollments_today_report = gtr.generate_verified_enrollment_count_today_report()
        audit_enrollment_report = gtr.generate_audit_enrollment_count_report()
        audit_enrollments_today_report = gtr.generate_audit_enrollment_count_today_report()

        msg = 'Successfully generated course reports.'
        log.info(msg)

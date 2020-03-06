import csv

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from course_modes.models import CourseMode
from courseware.models import StudentModule
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import Registration, UserProfile, CourseEnrollment

from .models import CountReport

from datetime import datetime, timedelta, time


def remove_reports(months=3, weeks=None, days=None):
    """
    handler for removing reports
    """
    period = datetime.now().date()
    if months:
        period = period - timedelta(days=30*months)
    if weeks:
        period = period - timedelta(days=7*weeks)
    if days:
        period = period - timedelta(days=days)

    reports = CountReport.objects.all()
    reports_exclude_month_newest = reports.exclude(created__gte=period)
    for report in reports_exclude_month_newest:
        report.delete()

    msg = "Finished removing reports."
    return msg, True

##################
# Course Counts #
#################

class CourseCountReportGenerator:
    """
    Class for generating course reports
    """
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    course_overviews = CourseOverview.objects.all()
    course_modes = CourseMode.objects.all()
    verified_courses = course_modes.filter(mode_slug='verified')
    total_enrollments = CourseEnrollment.objects.all()
    verified_enrollments = total_enrollments.filter(mode='verified')
    audit_enrollments = total_enrollments.filter(mode='audit')

    def generate_course_overview_count_report(self):
        """
        Method for generating reports
        """
        if self.course_overviews.exists():
            course_overview_count = self.course_overviews.count()
        else:
            course_overview_count = 0
        course_overview_count_report = CountReport(
            key="course_overview_count",
            count_value=course_overview_count
        ).save()
        return course_overview_count_report

    def generate_verified_course_count_report(self):
        """
        Method for generating reports
        """
        if self.verified_courses.exists():
            verified_course_count = self.verified_courses.count()
        else:
            verified_course_count = 0
        verified_course_count_report = CountReport(
            key="verified_course_count",
            count_value=verified_course_count
        ).save()
        return verified_course_count_report


    def generate_enrollment_count_report(self):
        """
        Method for generating reports
        """
        if self.total_enrollments.exists():
            enrollment_count = self.total_enrollments.count()
        else:
            enrollment_count = 0
        enrollment_count_report = CountReport(
            key="enrollment_count",
            count_value=enrollment_count
        ).save()
        return enrollment_count_report

    def generate_enrollment_count_today_report(self):
        """
        Method for generating reports
        """
        enrollments_today = self.total_enrollments.filter(created__lte=self.today_end).filter(created__gte=self.today_start)
        if enrollments_today.exists():
            enrollments_today_count = enrollments_today.count()
        else:
            enrollments_today_count = 0
        enrollments_today_count_report = CountReport(
            key="enrollments_today_count",
            count_value=enrollments_today_count
        ).save()
        return enrollments_today_count_report

    def generate_verified_enrollment_count_report(self):
        """
        Method for generating reports
        """
        if self.verified_enrollments.exists():
            verified_enrollment_count = self.verified_enrollments.count()
        else:
            verified_enrollment_count = 0
        verified_enrollment_count_report = CountReport(
            key="verified_enrollment_count",
            count_value=verified_enrollment_count
        ).save()
        return verified_enrollment_count_report

    def generate_verified_enrollment_count_today_report(self):
        """
        Method for generating reports
        """
        verified_enrollments_today = self.verified_enrollments.filter(created__lte=self.today_end).filter(created__gte=self.today_start)
        if verified_enrollments_today.exists():
            verified_enrollments_today_count = verified_enrollments_today.count()
        else:
            verified_enrollments_today_count = 0
        verified_enrollments_today_count_report = CountReport(
            key="verified_enrollments_today_count",
            count_value=verified_enrollments_today_count
        ).save()
        return verified_enrollments_today_count_report

    def generate_audit_enrollment_count_report(self):
        """
        Method for generating reports
        """
        if self.audit_enrollments.exists():
            audit_enrollment_count = self.audit_enrollments.count()
        else:
            audit_enrollment_count = 0
        audit_enrollment_count_report = CountReport(
            key="audit_enrollment_count",
            count_value=audit_enrollment_count
        ).save()
        return audit_enrollment_count_report

    def generate_audit_enrollment_count_today_report(self):
        """
        Method for generating reports
        """
        audit_enrollments_today = self.audit_enrollments.filter(created__lte=self.today_end).filter(created__gte=self.today_start)
        if audit_enrollments_today.exists():
            audit_enrollments_today_count = audit_enrollments_today.count()
        else:
            audit_enrollments_today_count = 0
        audit_enrollments_today_count_report = CountReport(
            key="audit_enrollments_today_count",
            count_value=audit_enrollments_today_count
        ).save()
        return audit_enrollments_today_count_report


class UserCountReportGenerator:
    """
    Class for generating user counts
    """
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    registrations = Registration.objects.all()
    users = User.objects.all()
    active_users = users.filter(is_active=True)
    inactive_users = users.filter(is_active=False)
    non_staff_users = active_users.filter(is_staff=False)
    staff_users = active_users.filter(is_staff=True)

    def generate_registration_count_report(self):
        """
        Method for generating registration count reports
        """
        if self.registrations.exists():
            registration_count = self.registrations.count()
        else:
            registration_count = 0
        registration_count_report = CountReport(
            key="registration_count",
            count_value=registration_count
        ).save()
        return registration_count_report

    def generate_registration_today_count_report(self):
        """
        Method for generating registration count reports
        """
        registrations_today = self.users.filter(date_joined__lte=self.today_end).filter(date_joined__gte=self.today_start)
        if registrations_today.exists():
            registrations_today_count = registrations_today.count()
        else:
            registrations_today_count = 0
        registrations_today_count_report = CountReport(
            key="registrations_today_count",
            count_value=registrations_today_count
        ).save()
        return registrations_today_count_report

    def generate_user_count_report(self):
        """
        Method for generating user_count reports
        """
        if self.users.exists():
            user_count = self.users.count()
        else:
            user_count = 0
        user_count_report = CountReport(
            key="user_count",
            count_value=user_count
        ).save()
        return user_count_report

    def generate_active_user_count_report(self):
        """
        Method for generating active_user_count reports
        """
        if self.active_users.exists():
            active_user_count = self.active_users.count()
        else:
            active_user_count = 0
        active_users_report = CountReport(
            key="active_user_count",
            count_value=active_user_count
        ).save()
        return active_users_report

    def generate_active_users_today_count_report(self):
        """
        Method for generating registration count reports
        """
        active_users_today = self.active_users.filter(date_joined__lte=self.today_end).filter(date_joined__gte=self.today_start)
        if active_users_today.exists():
            active_users_today_count = active_users_today.count()
        else:
            active_users_today_count = 0
        active_users_today_count_report = CountReport(
            key="active_users_today_count",
            count_value=active_users_today_count
        ).save()
        return active_users_today_count_report

    def generate_inactive_user_count_report(self):
        """
        Method for generating inactive_user_count reports
        """
        if self.inactive_users.exists():
            inactive_user_count = self.inactive_users.count()
        else:
            inactive_user_count = 0
        inactive_user_count_report = CountReport(
            key="inactive_user_count",
            count_value=inactive_user_count
        ).save()
        return inactive_user_count_report

    def generate_non_staff_user_count_report(self):
        """
        Method for generating non_staff_user_count reports
        """
        if self.non_staff_users.exists():
            non_staff_user_count = self.non_staff_users.count()
        else:
            non_staff_user_count = 0
        non_staff_user_count_report = CountReport(
            key="non_staff_user_count",
            count_value=non_staff_user_count
        ).save()
        return non_staff_user_count_report

    def generate_staff_user_count_report(self):
        """
        Method for generating staff_user_count reports
        """
        if self.staff_users.exists():
            staff_user_count = self.staff_users.count()
        else:
            staff_user_count = 0
        staff_user_count_report = CountReport(
            key="staff_user_count",
            count_value=staff_user_count
        ).save()
        return staff_user_count_report


def email_student_modules_durations(course_id):
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    course_key = CourseKey.from_string(c.course_id)
    try:
        course_overview = CourseOverview.get_from_id(course_key)
    except CourseOverview.DoesNotExist:
        raise Exception("CourseOverview does not exist.")

    enrollments = CourseEnrollment.objects.filter(course=course_overview)

    student_list = []
    for enrollment in enrollments:
        student_data = {}
        student_data['user'] = enrollment.user

        get_modules = StudentModule.objects.filter(course_id=CourseKey.from_string(course_id), student=enrollment.user)

        earliest_module = get_modules.order_by('created').first()
        lastest_module = get_modules.order_by('-modified').first()
        time_diff = lastest_module.modified - earliest_module.created

        student_data['duration'] = time_diff.total_seconds()

    file_name = '/home/ubuntu/tempfiles/sparta-list-of-users-problem-status-{}.csv'.format(course_id)
    with open(file_name, mode='w') as apps_file:
        writer = csv.writer(apps_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time generated:', tnow,])
        writer.writerow(['Username', 'Email', 'Duration'])
        for student in student_list:
            writer.writerow([student['user'].username, student['user'].email, student['duration']])

    email = EmailMessage(
    'Coursebank Student Modules Durations for course with ID {}'.format(course_id),
    'Attached file of Student Modules Durations ',
    'no-reply-coursebank-reports@coursebank.ph',
    ['junfel@buri.io',],
    )
    email.attach_file(file_name)
    email.send()

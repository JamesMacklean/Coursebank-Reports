"""
Modified ungenerated_cert command: fixed check_if_user_completed_course
Management command to find all students that need certificates for
courses that have finished, and put their cert requests on the queue.
"""
from __future__ import print_function
import datetime
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from opaque_keys.edx.keys import CourseKey
from pytz import UTC
from six import text_type

from lms.djangoapps.certificates.api import generate_user_certificates
from lms.djangoapps.certificates.models import CertificateStatuses, certificate_status_for_student
from lms.djangoapps.courseware.views.views import is_course_passed
from xmodule.modulestore.django import modulestore

# from sparta_pages.models import SpartaCourse
from coursebank_reports.helpers.helpers import check_if_user_completed_course

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to find all students that need certificates
    for courses that have finished and put their cert requests on the queue.
    """

    help = """
    Find all students that need certificates for courses that have finished and
    put their cert requests on the queue.

    If --user is given, only grade and certify the requested username.

    Use the --noop option to test without actually putting certificates on the
    queue to be generated.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--noop',
            action='store_true',
            dest='noop',
            help="Don't add certificate requests to the queue"
        )
        parser.add_argument(
            '--insecure',
            action='store_true',
            dest='insecure',
            help="Don't use https for the callback url to the LMS, useful in http test environments"
        )
        parser.add_argument(
            '-f', '--force-gen',
            metavar='STATUS',
            dest='force',
            default=False,
            help='Will generate new certificates for only those users whose entry in the certificate table matches '
            'STATUS. STATUS can be generating, unavailable, deleted, error or notpassing.'
        )
        parser.add_argument(
            '-c', '--course',
            metavar='COURSE_ID',
            dest='course',
            required=True,
            help='Grade and generate certificates for a specific course'
        )
        parser.add_argument(
            '-u', '--user',
            metavar='USERNAME',
            dest='user',
            help="Username to generate certificate for"
        )


    def handle(self, *args, **options):
        LOGGER.info(
            (
                u"Starting to create tasks for ungenerated certificates "
                u"with arguments %s and options %s"
            ),
            text_type(args),
            text_type(options)
        )

        # Will only generate a certificate if the current
        # status is in the unavailable state, can be set
        # to something else with the force flag

        if options['force']:
            valid_statuses = [getattr(CertificateStatuses, options['force'])]
        else:
            valid_statuses = [CertificateStatuses.unavailable]

        # Print update after this many students
        status_interval = 500

        ended_courses = []

        username = options.get('user', None)
        
        course = CourseKey.from_string(options['course'])
        ended_courses = [course,]

        # if course_id is not None:
        #     course = CourseKey.from_string(course_id)
        #     ended_courses = [course,]
        # else:
        #     for course in SpartaCourse.objects.filter(is_active=True):
        #         course_key = CourseKey.from_string(course.course_id)
        #         if course_key not in ended_courses:
        #             ended_courses.append(course_key)

        for course_key in ended_courses:
            self.stdout.write("Current generating certificate: {}".format(course_key))
            # prefetch all chapters/sequentials by saying depth=2
            course = modulestore().get_course(course_key, depth=2)

            enrolled_students = User.objects.filter(
                courseenrollment__course_id=course_key
            )

            if username is not None:
                enrolled_students = enrolled_students.filter(username=username)

            total = enrolled_students.count()
            count = 0
            start = datetime.datetime.now(UTC)

            for student in enrolled_students:
                count += 1
                if count % status_interval == 0:
                    # Print a status update with an approximation of
                    # how much time is left based on how long the last
                    # interval took
                    diff = datetime.datetime.now(UTC) - start
                    timeleft = diff * (total - count) / status_interval
                    hours, remainder = divmod(timeleft.seconds, 3600)
                    minutes, _seconds = divmod(remainder, 60)
                    print("{0}/{1} completed ~{2:02}:{3:02}m remaining".format(count, total, hours, minutes))
                    start = datetime.datetime.now(UTC)

                cert_status = certificate_status_for_student(student, course_key)['status']
                LOGGER.info(
                    (
                        u"Student %s has certificate status '%s' "
                        u"in course '%s'"
                    ),
                    student.id,
                    cert_status,
                    text_type(course_key)
                )

                if cert_status in valid_statuses:

                    if not options['noop']:

                        # generate certificate if student passed
                        if check_if_user_completed_course(student, text_type(course_key)) and is_course_passed(student, course):

                            # Add the certificate request to the queue
                            ret = generate_user_certificates(
                                student,
                                course_key,
                                course=course,
                                insecure=options['insecure']
                            )
                            
                            self.stdout.write("Generated certificate for User: {}".format(student.username))

                            if ret == 'generating':
                                LOGGER.info(
                                    (
                                        u"Added a certificate generation task to the XQueue "
                                        u"for student %s in course '%s'. "
                                        u"The new certificate status is '%s'."
                                    ),
                                    student.id,
                                    text_type(course_key),
                                    ret
                                )

                    else:
                        LOGGER.info(
                            (
                                u"Skipping certificate generation for "
                                u"student %s in course '%s' "
                                u"because the noop flag is set."
                            ),
                            student.id,
                            text_type(course_key)
                        )

                else:
                    LOGGER.info(
                        (
                            u"Skipped student %s because "
                            u"certificate status '%s' is not in %s"
                        ),
                        student.id,
                        cert_status,
                        text_type(valid_statuses)
                    )

            LOGGER.info(
                (
                    u"Completed ungenerated certificates command "
                    u"for course '%s'"
                ),
                text_type(course_key)
            )
            self.stdout.write("Finished generating certificate: {}".format(course_key))

import csv
from datetime import datetime
from django.utils import timezone
import logging
import unicodecsv

from django.core.mail import send_mail, EmailMessage

from django.http import Http404
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from opaque_keys.edx.keys import CourseKey
from student.models import CourseEnrollment, UserProfile
from lms.djangoapps.certificates.api import get_certificate_for_user
from openedx.core.djangoapps.course_groups.models import CourseUserGroup

LOGGER = logging.getLogger(__name__)

def export_learner_profiles_with_cohort(course_id, email_address=None):
    """"""
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    course_key = CourseKey.from_string(course_id)
    enrollments = CourseEnrollment.objects.filter(
        course_id=course_key,
        is_active=True
    )

    user_list = []
    for e in enrollments:

        cert = get_certificate_for_user(e.user.username, course_key)
        if cert is not None and cert['status'] == "downloadable":
            date_completed = cert['created'].strftime('%Y-%m-%dT%H:%M:%S.000Z')
        else:
            date_completed = ""

        cohort_groups = e.user.course_groups.filter(
            course_id=course_key
        )

        for g in cohort_groups:
            user_list.append({
                "name": e.user.profile.name,
                "email": e.user.email,
                "date_completed": date_completed,
                "cohort": g.name
            })

    file_name = '/home/ubuntu/tempfiles/export_learner_profiles_with_cohort_{}.csv'.format(tnow)
    with open(file_name, mode='w') as csv_file:
        writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
        writer.writerow([
            'Full Name',
            'Email',
            'Date of Completion',
            'Cohort'
            ])

        for u in user_list:
            writer.writerow([
                u['name'],
                u['email'],
                u['date_completed'],
                u['cohort']
                ])

    if email_address:
        email = EmailMessage(
            'Coursebank - Learner Profiles with Cohort',
            'Attached file of Learner Profiles with Cohort (as of {})'.format(tnow),
            'no-reply-learner-profiles-with-cohorts@coursebank.ph',
            [email_address,],
        )
        email.attach_file(file_name)
        email.send()

def export_learner_profiles(course_id, email_address=None):
    """"""
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    user_list = []

    if course_id is None:
        profiles = User.objects.all()

        for p in profiles:
            try:
                user_list.append({
                    "name": p.profile.name,
                    "username": p.username,
                    "email": p.email,
                    "created": p.date_joined,
                })
            except UserProfile.DoesNotExist:
                user_list.append({
                    "name": p.username,
                    "username": p.username,
                    "email": p.email,
                    "created": p.date_joined,
                })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Full Name',
                'Username',
                'Email',
                'Created'
                ])

            for u in user_list:
                writer.writerow([
                    u['name'],
                    u['username'],
                    u['email'],
                    u['created']
                    ])

        if email_address:
            email = EmailMessage(
                'Coursebank - Learner Profiles',
                'Attached file of Learner Profiles (as of {})'.format(tnow),
                'no-reply-learner-profiles@coursebank.ph',
                [email_address,],
            )
            email.attach_file(file_name)
            email.send()

    else:
        course_key = CourseKey.from_string(course_id)
        enrollments = CourseEnrollment.objects.filter(
            course_id=course_key,
            is_active=True
        )

        for e in enrollments:
            cert = get_certificate_for_user(e.user.username, course_key)
            if cert is not None and cert['status'] == "downloadable":
                date_completed = cert['created'].strftime('%Y-%m-%dT%H:%M:%S.000Z')
            else:
                date_completed = ""

            user_list.append({
                "name": e.user.profile.name,
                "username": e.user.username,
                "email": e.user.email,
                "created": e.user.date_joined,
                "last_login": e.user.last_login,
                "date_completed": date_completed
            })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Full Name',
                'Username',
                'Email',
                'Created',
                'Last Login',
                'Date Completed',
                ])

            for u in user_list:
                writer.writerow([
                    u['name'],
                    u['username'],
                    u['email'],
                    u['created'],
                    u['last_login'],
                    u['date_completed']
                    ])

        if email_address:
            email = EmailMessage(
                'Coursebank - Learner Profiles',
                'Attached file of Learner Profiles (as of {})'.format(tnow),
                'no-reply-learner-profiles@coursebank.ph',
                [email_address,],
            )
            email.attach_file(file_name)
            email.send()

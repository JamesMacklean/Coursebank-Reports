import csv
from datetime import datetime
from django.utils import timezone
import logging
import unicodecsv

from django.db import connection
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

def export_learner_profiles(active, course_id, email_address=None):
    """"""
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    user_list = []

    if course_id is None:
        if active == "yes":
          profiles = User.objects.filter(is_active=True)
        else:
          profiles = User.objects.all()

        for p in profiles:
            try:
                user_list.append({
                    "studentid": p.id,
                    "name": p.profile.name,
                    "username": p.username,
                    "email": p.email,
                    "created": p.date_joined,
                    "last_login": p.last_login,
                })
            except UserProfile.DoesNotExist:
                user_list.append({
                    "studentid": p.id,
                    "name": p.username,
                    "username": p.username,
                    "email": p.email,
                    "created": p.date_joined,
                    "last_login": p.last_login,
                })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Student ID',
                'Full Name',
                'Username',
                'Email',
                'Created',
                'Last Login'
                ])

            for u in user_list:
                writer.writerow([
                    u['studentid'],
                    u['name'],
                    u['username'],
                    u['email'],
                    u['created'],
                    u['last_login'],
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
                "studentid": e.user.id,
                "name": e.user.profile.name,
                "username": e.user.username,
                "email": e.user.email,
                "created": e.created,
                "last_login": e.user.last_login,
                "date_completed": date_completed
            })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Student ID',
                'Full Name',
                'Username',
                'Email',
                'Date Enrolled',
                'Last Login',
                'Date Completed',
                ])

            for u in user_list:
                writer.writerow([
                    u['studentid'],
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

def export_learner_demographics(active, course_id, email_address=None):
    """"""
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')

    user_list = []

    if course_id is None:
        if active == "yes":
          profiles = User.objects.filter(is_active=True)
        else:
          profiles = User.objects.all()

        for p in profiles:
            with connection.cursor() as cursor:
               cursor.execute("Select gender from auth_userprofile where user_id = %s", [p.id])
               person_gender = cursor.fetchone()
            with connection.cursor() as cursor:
               cursor.execute("Select year_of_birth from auth_userprofile where user_id = %s", [p.id])
               person_age = cursor.fetchone()
            with connection.cursor() as cursor:
               cursor.execute("Select country from auth_userprofile where user_id = %s", [p.id])
               person_location = cursor.fetchone()

            try:
                user_list.append({
                    "studentid": p.id,
                    "name": p.profile.name,
                    "username": p.username,
                    "email": p.email,
                    "gender": person_gender,
                    "birthyear": person_age,
                    "location": person_location,
                })
            except UserProfile.DoesNotExist:
                user_list.append({
                    "studentid": p.id,
                    "name": p.username,
                    "username": p.username,
                    "email": p.email,
                    "gender": person_gender,
                    "birthyear": person_age,
                    "location": person_location,
                })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Student ID',
                'Full Name',
                'Username',
                'Email',
                'Gender',
                'Birth Year',
                'Location',
                ])

            for u in user_list:
                writer.writerow([
                    u['studentid'],
                    u['name'],
                    u['username'],
                    u['email'],
                    u['gender'],
                    u['birthyear'],
                    u['location'],
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

            with connection.cursor() as cursor:
               cursor.execute("Select gender from auth_userprofile where user_id = %s", [e.user.id])
               person_gender = cursor.fetchone()
            with connection.cursor() as cursor:
               cursor.execute("Select year_of_birth from auth_userprofile where user_id = %s", [e.user.id])
               person_age = cursor.fetchone()
            with connection.cursor() as cursor:
               cursor.execute("Select country from auth_userprofile where user_id = %s", [e.user.id])
               person_location = cursor.fetchone()

            user_list.append({
                "studentid": e.user.id,
                "name": e.user.profile.name,
                "username": e.user.username,
                "email": e.user.email,
                "gender": person_gender,
                "birthyear": person_age,
                "location": person_location,
                "created": e.created,
            })
        file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
        with open(file_name, mode='w') as csv_file:
            writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
            writer.writerow([
                'Student ID',
                'Full Name',
                'Username',
                'Email',
                'Gender',
                'Birth Year',
                'Location',
                'Date Enrolled',
                ])

            for u in user_list:
                writer.writerow([
                    u['studentid'],
                    u['name'],
                    u['username'],
                    u['email'],
                    u['gender'],
                    u['birthyear'],
                    u['location'],
                    u['created'],
                    ])

        if email_address:
            email = EmailMessage(
                'Coursebank - Learner Profiles',
                'Attached file of Learner Demographics (as of {})'.format(tnow),
                'no-reply-learner-profiles@coursebank.ph',
                [email_address,],
            )
            email.attach_file(file_name)
            email.send()

def export_learner_pga(course_id, email_address=None):
    """"""
    tnow = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    user_list = []

    if course_id:
            with connection.cursor() as cursor:
                   cursor.execute("Select id, student_id from submissions_studentitem where course_id = %s", [course_id])
                   studentitems = cursor.fetchall()

            for items in studentitems:
                   result1 = items[0]
                   result2 = items[1]
                   item_id = result1
                   anonymous_user_id = result2

                   with connection.cursor() as cursor:
                        cursor.execute("Select uuid, attempt_number, submitted_at, raw_answer from submissions_submission where student_item_id = %s", [item_id])
                        studentitems = cursor.fetchone()
                        result1 = studentitems[0]
                        result2 = studentitems[1]
                        result3 = studentitems[2]
                        result4 = studentitems[3]
                        item_uuid = result1
                        attempt = result2
                        submission_date = result3
                        answer = result4

                   with connection.cursor() as cursor:
                        cursor.execute("Select user_id from student_anonymoususerid where anonymous_user_id = %s", [anonymous_user_id])
                        studentid = cursor.fetchone()
                        student_id = studentid

                   with connection.cursor() as cursor:
                        cursor.execute("Select auth_user.username, auth_user.email, auth_userprofile.name from auth_user INNER JOIN auth_userprofile ON auth_user.id=auth_userprofile.user_id where auth_user.id = %s", [student_id])
                        students = cursor.fetchone()
                        result1 = students[0]
                        result2 = students[1]
                        result3 = students[2]
                        student_username = result1
                        student_email = result2
                        student_name = result3

                   user_list.append({
                        "fullname": student_name,
                        "username": student_username,
                        "email": student_email,
                        "attempt": attempt,
                        "answer": answer,
                        "subm_date": submission_date,
                })


            file_name = '/home/ubuntu/tempfiles/export_learner_profiles_{}.csv'.format(tnow)
            with open(file_name, mode='w') as csv_file:
                   writer = unicodecsv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,  encoding='utf-8')
                   writer.writerow([
                        'Full Name',
                        'Username',
                        'Email',
                        'Attempts',
                        'Answer',
                        'Submission Date',
                  ])

                   for u in user_list:
                        writer.writerow([
                           u['fullname'],
                           u['username'],
                           u['email'],
                           u['attempt'],
                           u['answer'],
                           u['subm_date'],
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

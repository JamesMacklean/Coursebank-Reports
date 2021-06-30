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
    courseid = unicode(course_id)

    student_name = "john"
    student_username = "john"
    student_email = "sampleemail"
    attempt = 1
    answer = "sample"
    submission_date = "date"

    if courseid:
            with connection.cursor() as cursor:
                   cursor.execute("Select id from submissions_studentitem where course_id = %s", [courseid])
                   studentitems = cursor.fetchall()

            """for items in studentitems:
                   item_id = items[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select student_id from submissions_studentitem where id = %s AND course_id = %s", [item_id, courseid])
                        anon_user = cursor.fetchone()
                        anonymous_user_id = anon_user[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select uuid from submissions_submission where student_item_id = %s", [item_id])
                        itemid = cursor.fetchone()
                        item_uuid = itemid[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select attempt_number from submissions_submission where student_item_id = %s", [item_id])
                        attempt_num = cursor.fetchone()
                        attempt = attempt_num[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select submitted_at from submissions_submission where student_item_id = %s", [item_id])
                        subm = cursor.fetchone()
                        submission_date = subm[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select raw_answer from submissions_submission where student_item_id = %s", [item_id])
                        ans = cursor.fetchone()
                        answer = ans[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select user_id from student_anonymoususerid where anonymous_user_id = %s", [anonymous_user_id])
                        studentid = cursor.fetchone()
                        student_id = studentid[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select username from auth_user where id = %s", [student_id])
                        student_user = cursor.fetchone()
                        student_username = student_user[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select email from auth_user where id = %s", [student_id])
                        studentemail = cursor.fetchone()
                        student_email = studentemail[0]

                   with connection.cursor() as cursor:
                        cursor.execute("Select name from auth_userprofile where user_id = %s", [student_id])
                        studentname = cursor.fetchone()
                        student_name = studentname[0]"""

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

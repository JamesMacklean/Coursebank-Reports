from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import loader, Context
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import Registration, UserProfile, CourseEnrollment
from course_modes.models import CourseMode
from django.contrib.auth.models import User

from .models import CountReport

import datetime


@staff_member_required
def enrollments_reports_view(request):
    """
    View for count reports
    Expected to be used for graph rendering
    """
    context = {}
    queryset = CountReport.objects.all()
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_month = today - datetime.timedelta(days=30)

    # CourseEnrollments
    enrollment_reports = queryset.filter(key="enrollment_count")
    enrollment_reports_week = enrollment_reports.filter(created__gte=last_week).order_by('created')
    enrollment_reports_month = enrollment_reports.filter(created__gte=last_month).order_by('created')
    context['enrollment_reports'] = enrollment_reports
    context['enrollment_reports_latest'] = enrollment_reports.first()
    context['enrollment_reports_week'] = enrollment_reports_week
    context['enrollment_reports_month'] = enrollment_reports_month

    # Daily CourseEnrollments
    enrollments_daily_reports = queryset.filter(key="enrollments_today_count")
    enrollments_daily_reports_week = enrollments_daily_reports.filter(created__gte=last_week).order_by('created')
    enrollments_daily_reports_month = enrollments_daily_reports.filter(created__gte=last_month).order_by('created')
    context['enrollments_daily_reports'] = enrollments_daily_reports
    context['enrollments_daily_reports_latest'] = enrollments_daily_reports.first()
    context['enrollments_daily_reports_week'] = enrollments_daily_reports_week
    context['enrollments_daily_reports_month'] = enrollments_daily_reports_month

    # Verified CourseEnrollments
    verified_enrollment_reports = queryset.filter(key="verified_enrollment_count")
    verified_enrollment_reports_week = verified_enrollment_reports.filter(created__gte=last_week).order_by('created')
    verified_enrollment_reports_month = verified_enrollment_reports.filter(created__gte=last_month).order_by('created')
    context['verified_enrollment_reports'] = verified_enrollment_reports
    context['verified_enrollment_reports_latest'] = verified_enrollment_reports.first()
    context['verified_enrollment_reports_week'] = verified_enrollment_reports_week
    context['verified_enrollment_reports_month'] = verified_enrollment_reports_month

    # Daily Verified CourseEnrollments
    verified_enrollments_daily_reports = queryset.filter(key="verified_enrollments_today_count")
    verified_enrollments_daily_reports_week = verified_enrollments_daily_reports.filter(created__gte=last_week).order_by('created')
    verified_enrollments_daily_reports_month = verified_enrollments_daily_reports.filter(created__gte=last_month).order_by('created')
    context['verified_enrollments_daily_reports'] = verified_enrollments_daily_reports
    context['verified_enrollments_daily_reports_latest'] = verified_enrollments_daily_reports.first()
    context['verified_enrollments_daily_reports_week'] = verified_enrollments_daily_reports_week
    context['verified_enrollments_daily_reports_month'] = verified_enrollments_daily_reports_month

    # Audit CourseEnrollments
    audit_enrollment_reports = queryset.filter(key="audit_enrollment_count")
    audit_enrollment_reports_week = audit_enrollment_reports.filter(created__gte=last_week).order_by('created')
    audit_enrollment_reports_month = audit_enrollment_reports.filter(created__gte=last_month).order_by('created')
    context['audit_enrollment_reports'] = audit_enrollment_reports
    context['audit_enrollment_reports_latest'] = audit_enrollment_reports.first()
    context['audit_enrollment_reports_week'] = audit_enrollment_reports_week
    context['audit_enrollment_reports_month'] = audit_enrollment_reports_month

    # Daily Audit CourseEnrollments
    audit_enrollments_daily_reports = queryset.filter(key="audit_enrollments_today_count")
    audit_enrollments_daily_reports_week = audit_enrollments_daily_reports.filter(created__gte=last_week).order_by('created')
    audit_enrollments_daily_reports_month = audit_enrollments_daily_reports.filter(created__gte=last_month).order_by('created')
    context['audit_enrollments_daily_reports'] = audit_enrollments_daily_reports
    context['audit_enrollments_daily_reports_latest'] = audit_enrollments_daily_reports.first()
    context['audit_enrollments_daily_reports_week'] = audit_enrollments_daily_reports_week
    context['audit_enrollments_daily_reports_month'] = audit_enrollments_daily_reports_month

    return render(request, 'coursebank_reports/enrollments-reports.html', context)


@staff_member_required
def user_reports_view(request):
    """
    View for count reports
    Expected to be used for graph rendering
    """
    context = {}
    queryset = CountReport.objects.all()
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    last_month = today - datetime.timedelta(days=30)

    # Total Users
    user_reports = queryset.filter(key="user_count")
    user_reports_week = user_reports.filter(created__gte=last_week).order_by('created')
    user_reports_month = user_reports.filter(created__gte=last_month).order_by('created')
    context['user_reports'] = user_reports
    context['user_reports_latest'] = user_reports.first()
    context['user_reports_week'] = user_reports_week
    context['user_reports_month'] = user_reports_month

    # Daily Registrations
    registration_daily_reports = queryset.filter(key="registrations_today_count")
    registration_daily_reports_week = registration_daily_reports.filter(created__gte=last_week).order_by('created')
    registration_daily_reports_month = registration_daily_reports.filter(created__gte=last_month).order_by('created')
    context['registration_daily_reports'] = registration_daily_reports
    context['registration_daily_reports_latest'] = registration_daily_reports.first()
    context['registration_daily_reports_week'] = registration_daily_reports_week
    context['registration_daily_reports_month'] = registration_daily_reports_month

    # Active Users
    active_reports = queryset.filter(key="active_user_count")
    active_reports_week = active_reports.filter(created__gte=last_week).order_by('created')
    active_reports_month = active_reports.filter(created__gte=last_month).order_by('created')
    context['active_reports'] = active_reports
    context['active_reports_latest'] = active_reports.first()
    context['active_reports_week'] = active_reports_week
    context['active_reports_month'] = active_reports_month

    # Daily Active Users
    active_daily_reports = queryset.filter(key="active_users_today_count")
    active_daily_reports_week = active_daily_reports.filter(created__gte=last_week).order_by('created')
    active_daily_reports_month = active_daily_reports.filter(created__gte=last_month).order_by('created')
    context['active_daily_reports'] = active_daily_reports
    context['active_daily_reports_latest'] = active_daily_reports.first()
    context['active_daily_reports_week'] = active_daily_reports_week
    context['active_daily_reports_month'] = active_daily_reports_month

    return render(request, 'coursebank_reports/user-reports.html', context)


@staff_member_required
def index_reports(request):
    """
    View for overall reports
    """
    registrations = Registration.objects.all()
    users = User.objects.all()
    active_users = users.filter(is_active=True)
    inactive_users = users.filter(is_active=False)
    non_staff_users = active_users.filter(is_staff=False)
    staff_users = active_users.filter(is_staff=True)
    total_enrollments = CourseEnrollment.objects.all()
    verified_enrollments = total_enrollments.filter(mode='verified')
    audit_enrollments = total_enrollments.filter(mode='audit')
    courses = CourseOverview.objects.all()
    course_modes = CourseMode.objects.all()
    verified_courses = course_modes.filter(mode_slug='verified')

    context = {
        'registration_count': registrations.count(),
        'total_user_count': users.count(),
        'active_user_count': active_users.count(),
        'inactive_user_count': inactive_users.count(),
        'total_enrollment_count': total_enrollments.count(),
        'audit_enrollment_count': audit_enrollments.count(),
        'verified_enrollment_count': verified_enrollments.count(),
        'non_staff_user_count': non_staff_users.count(),
        'staff_user_count': staff_users.count(),
        'course_count': courses.count(),
        'verified_courses_count': verified_courses.count(),
    }
    return render(request, 'coursebank_reports/reports.html', context)


@staff_member_required
def course_list_view(request):
    queryset = CourseOverview.objects.all()

    filter_org = request.GET.get('filter_org', None)
    if filter_org is not None and filter_org != '':
        queryset = queryset.filter(org__contains=filter_org)

    filter_display_name = request.GET.get('filter_display_name', None)
    if filter_display_name is not None and filter_display_name != '':
        queryset = queryset.filter(display_name__contains=filter_display_name)

    if queryset.exists():
        course_count = queryset.count()
    else:
        course_count = 0

    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    try:
        course_list = paginator.page(page)
    except PageNotAnInteger:
        course_list = paginator.page(1)
    except EmptyPage:
        course_list = paginator.page(paginator.num_pages)

    num_pages = paginator.num_pages
    page_range = paginator.page_range

    is_paginated = True if course_count > 100 else False

    context = {
        'course_list': course_list,
        'num_pages': num_pages,
        'page_range': page_range,
        'is_paginated': is_paginated,
        'course_count': course_count
    }
    return render(request, 'coursebank_reports/courses.html', context)


@staff_member_required
def enrollment_list_view(request, course_id, export_csv=False):
    queryset = CourseEnrollment.objects.all()
    course_key = CourseKey.from_string(course_id)
    try:
        course = CourseOverview.get_from_id(course_key)
    except CourseOverview.DoesNotExist:
        raise Http404
    queryset = queryset.filter(course=course)

    filter_username = request.GET.get('filter_username', None)
    if filter_username is not None and filter_username != '':
        queryset = queryset.filter(user__username=filter_username)

    filter_email = request.GET.get('filter_email', None)
    if filter_email is not None and filter_email != '':
        queryset = queryset.filter(user__email=filter_email)

    filter_mode = request.GET.get('filter_mode', None)
    if filter_mode is not None and filter_mode != '':
        if filter_mode != 'all':
            queryset = queryset.filter(mode=filter_mode)

    filter_active = request.GET.get('filter_active', None)
    if filter_active is not None and filter_active != '':
        if filter_active == 'active':
            queryset = queryset.filter(is_active=True)
        elif filter_active == 'inactive':
            queryset = queryset.filter(is_active=False)

    if queryset.exists():
        enrollment_count = queryset.count()
    else:
        enrollment_count = 0

    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    try:
        enrollment_list = paginator.page(page)
    except PageNotAnInteger:
        enrollment_list = paginator.page(1)
    except EmptyPage:
        enrollment_list = paginator.page(paginator.num_pages)

    num_pages = paginator.num_pages
    page_range = paginator.page_range

    is_paginated = True if enrollment_count > 100 else False

    context = {
        'course': course,
        'enrollment_list': enrollment_list,
        'num_pages': num_pages,
        'page_range': page_range,
        'is_paginated': is_paginated,
        'enrollment_count': enrollment_count
    }

    if export_csv:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enrollmentslist.csv"'
        csv_data = (
            ('username', 'email', 'mode', 'created', 'is_active'),
        )
        for enrollment in queryset:
            tuple = (
                "{}".format(enrollment.user.username),
                "{}".format(enrollment.user.email),
                "{}".format(enrollment.mode),
                "{}".format(enrollment.created),
                "{}".format(enrollment.is_active),
            )
            csv_data += (tuple,)
        t = loader.get_template('coursebank_reports/enrollment_csv_template.txt')
        csv_ctx = {
            'data': csv_data,
        }
        response.write(t.render(csv_ctx))
        return response

    return render(request, 'coursebank_reports/enrollments.html', context)

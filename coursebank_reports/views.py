from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import Registration, UserProfile, CourseEnrollment
from course_modes.models import CourseMode
from django.contrib.auth.models import User

from .models import CountReport

import datetime


# @staff_member_required
# def course_reports_view(request):
#     """
#     View for count reports
#     Expected to be used for graph rendering
#     """
#     context = {}
#     queryset = CountReport.objects.all()
#     today = datetime.date.today()
#     last_week = today - datetime.timedelta(days=7)
#     last_month = today - datetime.timedelta(days=30)
#
#     # Course Overviews
#     course_reports = queryset.filter(key="course_overview_count")
#     course_reports_week = course_reports.filter(created__gte=last_week)
#     course_reports_month = course_reports.filter(created__gte=last_month)
#     context['course_reports'] = course_reports
#     context['course_reports_latest'] = course_reports[0]
#     context['course_reports_week'] = course_reports_week[:7]
#     context['course_reports_month'] = course_reports_month[:30]
#
#     # Verified Courses (CourseModes)
#     verified_course_reports = queryset.filter(key="verified_course_count")
#     verified_course_reports_week = verified_course_reports.filter(created__gte=last_week)
#     verified_course_reports_month = verified_course_reports.filter(created__gte=last_month)
#     context['verified_course_reports'] = verified_course_reports
#     context['verified_course_reports_latest'] = verified_course_reports[0]
#     context['verified_course_reports_week'] = verified_course_reports_week[:7]
#     context['verified_course_reports_month'] = verified_course_reports_month[:30]
#
#     return render(request, 'coursebank_reports/course-reports.html', context)


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
    enrollment_reports_week = enrollment_reports.filter(created__gte=last_week)
    enrollment_reports_month = enrollment_reports.filter(created__gte=last_month)
    context['enrollment_reports'] = enrollment_reports
    context['enrollment_reports_latest'] = enrollment_reports[0]
    context['enrollment_reports_week'] = enrollment_reports_week[:7]
    context['enrollment_reports_month'] = enrollment_reports_month[:30]

    # Daily CourseEnrollments
    enrollments_daily_reports = queryset.filter(key="enrollments_today_count")
    enrollments_daily_reports_week = enrollments_daily_reports.filter(created__gte=last_week)
    enrollments_daily_reports_month = enrollments_daily_reports.filter(created__gte=last_month)
    context['enrollments_daily_reports'] = enrollments_daily_reports
    context['enrollments_daily_reports_latest'] = enrollments_daily_reports[0]
    context['enrollments_daily_reports_week'] = enrollments_daily_reports_week[:7]
    context['enrollments_daily_reports_month'] = enrollments_daily_reports_month[:30]

    # Verified CourseEnrollments
    verified_enrollment_reports = queryset.filter(key="verified_enrollment_count")
    verified_enrollment_reports_week = verified_enrollment_reports.filter(created__gte=last_week)
    verified_enrollment_reports_month = verified_enrollment_reports.filter(created__gte=last_month)
    context['verified_enrollment_reports'] = verified_enrollment_reports
    context['verified_enrollment_reports_latest'] = verified_enrollment_reports[0]
    context['verified_enrollment_reports_week'] = verified_enrollment_reports_week[:7]
    context['verified_enrollment_reports_month'] = verified_enrollment_reports_month[:30]

    # Daily Verified CourseEnrollments
    verified_enrollments_daily_reports = queryset.filter(key="verified_enrollments_today_count")
    verified_enrollments_daily_reports_week = verified_enrollments_daily_reports.filter(created__gte=last_week)
    verified_enrollments_daily_reports_month = verified_enrollments_daily_reports.filter(created__gte=last_month)
    context['verified_enrollments_daily_reports'] = verified_enrollments_daily_reports
    context['verified_enrollments_daily_reports_latest'] = verified_enrollments_daily_reports[0]
    context['verified_enrollments_daily_reports_week'] = verified_enrollments_daily_reports_week[:7]
    context['verified_enrollments_daily_reports_month'] = verified_enrollments_daily_reports_month[:30]

    # Audit CourseEnrollments
    audit_enrollment_reports = queryset.filter(key="audit_enrollment_count")
    audit_enrollment_reports_week = audit_enrollment_reports.filter(created__gte=last_week)
    audit_enrollment_reports_month = audit_enrollment_reports.filter(created__gte=last_month)
    context['audit_enrollment_reports'] = audit_enrollment_reports
    context['audit_enrollment_reports_latest'] = audit_enrollment_reports[0]
    context['audit_enrollment_reports_week'] = audit_enrollment_reports_week[:7]
    context['audit_enrollment_reports_month'] = audit_enrollment_reports_month[:30]

    # Daily Audit CourseEnrollments
    audit_enrollments_daily_reports = queryset.filter(key="audit_enrollments_today_count")
    audit_enrollments_daily_reports_week = audit_enrollments_daily_reports.filter(created__gte=last_week)
    audit_enrollments_daily_reports_month = audit_enrollments_daily_reports.filter(created__gte=last_month)
    context['audit_enrollments_daily_reports'] = audit_enrollments_daily_reports
    context['audit_enrollments_daily_reports_latest'] = audit_enrollments_daily_reports[0]
    context['audit_enrollments_daily_reports_week'] = audit_enrollments_daily_reports_week[:7]
    context['audit_enrollments_daily_reports_month'] = audit_enrollments_daily_reports_month[:30]

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
    user_reports_week = user_reports.filter(created__gte=last_week)
    user_reports_month = user_reports.filter(created__gte=last_month)
    context['user_reports'] = user_reports
    context['user_reports_latest'] = user_reports[0]
    context['user_reports_week'] = user_reports_week[:7]
    context['user_reports_month'] = user_reports_month[:30]

    # Daily Registrations
    registration_daily_reports = queryset.filter(key="registrations_today_count")
    registration_daily_reports_week = registration_daily_reports.filter(created__gte=last_week)
    registration_daily_reports_month = registration_daily_reports.filter(created__gte=last_month)
    context['registration_daily_reports'] = registration_daily_reports
    context['registration_daily_reports_latest'] = registration_daily_reports[0]
    context['registration_daily_reports_week'] = registration_daily_reports_week[:7]
    context['registration_daily_reports_month'] = registration_daily_reports_month[:30]

    # Active Users
    active_reports = queryset.filter(key="active_user_count")
    active_reports_week = active_reports.filter(created__gte=last_week)
    active_reports_month = active_reports.filter(created__gte=last_month)
    context['active_reports'] = active_reports
    context['active_reports_latest'] = active_reports[0]
    context['active_reports_week'] = active_reports_week[:7]
    context['active_reports_month'] = active_reports_month[:30]

    # Daily Active Users
    active_daily_reports = queryset.filter(key="active_users_today_count")
    active_daily_reports_week = active_daily_reports.filter(created__gte=last_week)
    active_daily_reports_month = active_daily_reports.filter(created__gte=last_month)
    context['active_daily_reports'] = active_daily_reports
    context['active_daily_reports_latest'] = active_daily_reports[0]
    context['active_daily_reports_week'] = active_daily_reports_week[:7]
    context['active_daily_reports_month'] = active_daily_reports_month[:30]

    return render(request, 'coursebank_reports/user-reports.html', context)


# @staff_member_required
# def count_reports(request):
#     """
#     View for count reports
#     Expected to be used for graph rendering
#     """
#     context = {}
#     queryset = CountReport.objects.all()
#     today = datetime.date.today()
#     last_week = today - datetime.timedelta(days=7)
#     last_month = today - datetime.timedelta(days=30)
#
#     # Registrations
#     registration_reports = queryset.filter(key="registration_count")
#     registration_reports_week = registration_reports.filter(created__gte=last_week)
#     registration_reports_month = registration_reports.filter(created__gte=last_month)
#     context['registration_reports'] = registration_reports
#     context['registration_reports_latest'] = registration_reports[0]
#     context['registration_reports_week'] = registration_reports_week[:7]
#     context['registration_reports_month'] = registration_reports_month[:30]
#
#     # Inactive Users
#     inactive_reports = queryset.filter(key="inactive_user_count")
#     inactive_reports_week = inactive_reports.filter(created__gte=last_week)
#     inactive_reports_month = inactive_reports.filter(created__gte=last_month)
#     context['inactive_reports'] = inactive_reports
#     context['inactive_reports_latest'] = inactive_reports[0]
#     context['inactive_reports_week'] = inactive_reports_week[:7]
#     context['inactive_reports_month'] = inactive_reports_month[:30]
#
#     # Non-Staff (Regular) Users
#     non_staff_reports = queryset.filter(key="non_staff_user_count")
#     non_staff_reports_week = non_staff_reports.filter(created__gte=last_week)
#     non_staff_reports_month = non_staff_reports.filter(created__gte=last_month)
#     context['non_staff_reports'] = non_staff_reports
#     context['non_staff_reports_latest'] = non_staff_reports[0]
#     context['non_staff_reports_week'] = non_staff_reports_week[:7]
#     context['non_staff_reports_month'] = non_staff_reports_month[:30]
#
#     # Staff (staff, superuser roles) Users
#     staff_reports = queryset.filter(key="staff_user_count")
#     staff_reports_week = staff_reports.filter(created__gte=last_week)
#     staff_reports_month = staff_reports.filter(created__gte=last_month)
#     context['staff_reports'] = staff_reports
#     context['staff_reports_latest'] = staff_reports[0]
#     context['staff_reports_week'] = staff_reports_week[:7]
#     context['staff_reports_month'] = staff_reports_month[:30]
#
#     return render(request, 'coursebank_reports/counts.html', context)


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

    filter_org = request.GET.get('filter_org')
    if filter_org:
        queryset = queryset.filter(org__contains=filter_org)

    filter_display_name = request.GET.get('filter_display_name')
    if filter_display_name:
        queryset = queryset.filter(display_name__contains=filter_display_name)

    if queryset.exists():
        course_count = queryset.count()
    else:
        course_count = 0

    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    course_list = paginator.get_page(page)
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
def enrollment_list_view(request, course_id):
    queryset = CourseEnrollment.objects.all()
    try:
        course = CourseOverview.get_from_id(course_id)
    except CourseOverview.DoesNotExist:
        raise Http404
    queryset = queryset.filter(course=course)

    filter_username = request.GET.get('filter_username')
    if filter_username:
        queryset = queryset.filter(user__username=filter_username)

    filter_email = request.GET.get('filter_email')
    if filter_email:
        queryset = queryset.filter(user__email=filter_email)

    filter_mode = request.GET.get('filter_mode')
    if filter_mode:
        if filter_mode != 'all':
            queryset = queryset.filter(mode=filter_mode)

    filter_active = request.GET.get('filter_active')
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
    enrollment_list = paginator.get_page(page)
    num_pages = paginator.num_pages
    page_range = paginator.page_range

    is_paginated = True if enrollment_count > 100 else False

    context = {
        'course': course,
        'enrollment_list': enrollment_list,
        'num_pages': num_pages,
        'page_range': page_range,
        'is_paginated': is_paginated,
        'enrollment_count': queryset.count()
    }
    return render(request, 'coursebank_reports/enrollments.html', context)


@method_decorator(staff_member_required, name='dispatch')
class EnrollmentListView(ListView):
    model = CourseEnrollment
    template_name = "coursebank_reports/enrollments.html"
    context_object_name = 'enrollment'
    paginate_by = 100

    def get_queryset(self):
        queryset = CourseEnrollment.objects.all()
        course_id = self.kwargs.get('course_id')
        try:
            course = CourseOverview.get_from_id(course_id)
        except CourseOverview.DoesNotExist:
            raise Http404
        queryset = queryset.filter(course=course)

        filter_username = self.request.GET.get('filter_username')
        if filter_username:
            queryset = queryset.filter(user__username=filter_username)

        filter_email = self.request.GET.get('filter_email')
        if filter_email:
            queryset = queryset.filter(user__email=filter_email)

        filter_mode = self.request.GET.get('filter_mode')
        if filter_mode:
            if filter_mode != 'all':
                queryset = queryset.filter(mode=filter_mode)

        filter_active = self.request.GET.get('filter_active')
        if filter_active == 'active':
            queryset = queryset.filter(is_active=True)
        elif filter_active == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(EnrollmentListView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        try:
            course = CourseOverview.get_from_id(course_id)
        except CourseOverview.DoesNotExist:
            raise Http404

        context['course'] = course
        return context


@staff_member_required
def course_enrollments_reports(request, course_id):
    """
    View for reports regarding a specific course
    CourseEnrollment:
    -user
    -course (CourseOverview)
    	-course_id
    -created
    -is_active
    -mode (CourseMode.DEFAULT_MODE_SLUG)
    -objects:
    	-num_enrolled_in(course_id)
    	-num_enrolled_exclude_admins(course_id)
    	-is_course_full::bool
    	-users_enrolled_in(course_id, include_inactive=False)::<queryset:Users>
    	-enrollment_counts(course_id)::<dict:{'total':<int>,'mode':<int>,..}
    """
    try:
        course = CourseOverview.get_from_id(course_id)
    except CourseOverview.DoesNotExist:
        raise Http404

    course_enrollments_list = CourseEnrollment.objects.filter(course_id=course_id)
    paginator = Paginator(course_enrollments_list, 100)
    page = request.GET.get('page')
    course_enrollments = paginator.get_page(page)
    num_pages = paginator.num_pages
    page_range = paginator.page_range

    context = {
        'course': course,
        'course_enrollments': course_enrollments,
        'num_pages': num_pages,
        'page_range': page_range
    }
    return render(request, 'coursebank_reports/enrollments.html', context)


@staff_member_required
def num_enrolled_reports(request, course_id):
    """
    View for reports regarding a specific course
    """
    try:
        course = CourseOverview.get_from_id(course_id)
    except CourseOverview.DoesNotExist:
        raise Http404

    exclude_admins = False
    exclude_admins_param = request.GET.get('exclude_admins', None)
    if exclude_admins_param is not None:
        param = exclude_admins_param.upper()
        if param == "TRUE" or param == "YES":
            exclude_admins = True

    if exclude_admins:
        num_enrolled_in = CourseEnrollment.objects.num_enrolled_exclude_admins(course_id)
    else:
        num_enrolled_in = CourseEnrollment.objects.num_enrolled_in(course_id)

    context = {
        'course': course,
        'num_enrolled_in': num_enrolled_in
    }
    return render(request, 'coursebank_reports/enrollments-num.html', context)


@staff_member_required
def enrollment_counts_reports(request, course_id):
    """
    View for reports regarding a specific course
    """
    try:
        course = CourseOverview.get_from_id(course_id)
    except CourseOverview.DoesNotExist:
        raise Http404

    enrollment_counts = CourseEnrollment.objects.enrollment_counts(course_id)

    context = {
        'course': course,
        'enrollment_counts': enrollment_counts
    }

    for key, value in enrollment_counts:
        context[key] = value

    return render(request, 'coursebank_reports/enrollments-count.html', context)


@staff_member_required
def enrollments_users_reports(request, course_id):
    """
    View for reports regarding a specific course
    """
    try:
        course = CourseOverview.get_from_id(course_id)
    except CourseOverview.DoesNotExist:
        raise Http404

    include_inactive = False
    include_inactive_param = request.GET.get('include_inactive', None)
    if include_inactive_param is not None:
        param = include_inactive_param.upper()
        if param == "TRUE" or param == "YES":
            include_inactive = True

    users_enrolled_in_list = CourseEnrollment.objects.users_enrolled_in(course_id, include_inactive=include_inactive)
    paginator = Paginator(users_enrolled_in_list, 100)
    page = request.GET.get('page')
    users_enrolled_in = paginator.get_page(page)
    num_pages = paginator.num_pages
    page_range = paginator.page_range

    context = {
        'course': course,
        'users_enrolled_in': users_enrolled_in,
        'num_pages': num_pages,
        'page_range': page_range
    }
    return render(request, 'coursebank_reports/enrollments-users.html', context)


@method_decorator(staff_member_required, name='dispatch')
class UserProfileDetailView(DetailView):
    """
    User:
    -username
    -email
    -is_staff
    -is_active
    -last_login
    -date_joined

    UserProfile:
    -user
    -name
    -year_of_birth
    	-age
    -gender
    	-gender_display
    -level_of_education
    	-level_of_education_display
    -country
    -allow_certificate
    """
    model = UserProfile
    template_name = 'coursebank_reports/profile.html'
    context_object_name = 'user'
    slug_field = 'user__id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        return context

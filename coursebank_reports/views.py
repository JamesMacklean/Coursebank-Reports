from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import Registration, UserProfile, CourseEnrollment
from course_modes.models import CourseMode

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


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
    verified_enrollments = enrollments.filter(mode='verified')
    audit_enrollments = enrollments.filter(mode='audit')
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


class CourseListView(ListView):
    model = CourseOverview
    template_name = "coursebank_reports/courses.html"
    context_object_name = 'course'
    paginate_by = 100

    @staff_member_required
    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['count'] = queryset.count()
        return context


class EnrollmentListView(ListView):
    model = CourseEnrollment
    template_name = "coursebank_reports/enrollments.html"
    context_object_name = 'enrollment'
    paginate_by = 100

    def get_queryset(self):
        queryset = CourseEnrollment.objects.all()
        course_id = self.kwargs.get('course_id', 'all')
        if course_id != 'all':
            queryset = queryset.filter(course_id=course_id)

        username = self.request.GET.get('username', None)
        email = self.request.GET.get('email', None)
        is_active = self.request.GET.get('is_active', None)
        mode = self.request.GET.get('mode', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        if email is not None:
            queryset = queryset.filter(user__email=email)
        if is_active is not None:
            if is_active.upper() == 'TRUE':
                queryset = queryset.filter(is_active=True)
            elif is_active.upper() == 'FALSE':
                queryset = queryset.filter(is_active=False)
        if mode is not None:
            queryset = queryset.filter(mode=mode)

        filter_username = self.request.GET.get('filter_username')
        if filter_username:
            queryset = queryset.filter(user__username=filter_username)

        filter_email = self.request.GET.get('filter_email')
        if filter_email:
            queryset = queryset.filter(user__email=filter_email)

        filter_mode = self.request.GET.get('filter_mode')
        if filter_mode != 'all':
            queryset = queryset.filter(mode=filter_mode)

        filter_active = self.request.GET.get('filter_active')
        if filter_active == 'active':
            queryset = queryset.filter(is_active=True)
        elif filter_active == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset

    @staff_member_required
    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)

        try:
            course = CourseOverview.get_from_id(course_id)
        except CourseOverview.DoesNotExist:
            raise Http404

        queryset = self.get_queryset()
        count = queryset.count()

        context['course'] = course
        context['count'] = count
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

    @staff_member_required
    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        return context

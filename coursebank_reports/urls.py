from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reports/$', views.index_reports, name='index-reports'),
    url(r'^reports/registrations/', views.RegistrationListView.as_view(), name='registration-reports'),
    url(r'^reports/profiles/', views.ProfileListView.as_view(), name='profile-reports'),
    url(r'^reports/courses/', views.CourseListView.as_view(), name='course-reports'),

    url(r'^reports/course/{}/enrollments/'.format(settings.COURSE_ID_PATTERN), views.EnrollmentListView.as_view(), name='course-enrollments-reports'),

    url(r'^reports/course/{}/enrollments/numbers/$'.format(settings.COURSE_ID_PATTERN), views.num_enrolled_reports, name='course-enrollments-reports'),
    url(r'^reports/course/{}/enrollments/counts/$'.format(settings.COURSE_ID_PATTERN), views.enrollment_counts_reports, name='course-enrollments-reports'),
    url(r'^reports/course/{}/enrollments/users/$'.format(settings.COURSE_ID_PATTERN), views.enrollments_users_reports, name='course-enrollments-reports'),
]

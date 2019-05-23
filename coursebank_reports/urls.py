from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reports/$', views.index_reports, name='index-reports'),
    url(r'^reports/courses/', views.course_list_view, name='course-reports'),
    url(r'^reports/course/{}/enrollments/'.format(settings.COURSE_ID_PATTERN), views.enrollment_list_view, name='course-enrollments-reports'),

    url(r'^reports/course/{}/enrollments/user/(?P<id>\d+)$'.format(settings.COURSE_ID_PATTERN), views.UserProfileDetailView.as_view(), name='course-enrollments-user-detail'),

    url(r'^reports/course/{}/enrollments/numbers/$'.format(settings.COURSE_ID_PATTERN), views.num_enrolled_reports, name='num-enrolled-reports'),
    url(r'^reports/course/{}/enrollments/counts/$'.format(settings.COURSE_ID_PATTERN), views.enrollment_counts_reports, name='enrollment-counts-reports'),
    url(r'^reports/course/{}/enrollments/users/$'.format(settings.COURSE_ID_PATTERN), views.enrollments_users_reports, name='enrollment-users-reports'),
]

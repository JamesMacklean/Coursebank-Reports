from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reports/$', views.index_reports, name='index-reports'),
    url(r'^reports/enrollments/$', views.enrollments_reports_view, name='enrollments-reports'),
    url(r'^reports/users/$', views.user_reports_view, name='user-reports'),

    url(r'^reports/courses/', views.course_list_view, name='course-reports'),
    url(r'^reports/course/{}/enrollments/'.format(settings.COURSE_ID_PATTERN), views.enrollment_list_view, name='course-enrollments-reports'),
]

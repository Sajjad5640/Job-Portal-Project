from django.urls import path
from JobPortal.views import *


urlpatterns = [
    path('register/',register_page,name='register_page'),
    path('login-page/',login_page,name='login_page'),
    path('',dashboard_page,name='dashboard_page'),
    path('logout-page/',logout_page,name='logout_page'),
    path('profile-page/',profile_page,name='profile_page'),
    path('update-profile/',update_profile,name='update_profile'),
    path('browse-job-view/',browse_job_view,name='browse_job_view'),
    path('post-job-view/',post_job_view,name='post_job_view'),
    path('update-job-view/<int:id>/',update_job_view,name='update_job_view'),
    path('delete-job-view/<int:id>/',delete_job_view,name='delete_job_view'),
    path('apply-job-view/<int:id>/',apply_job_view,name='apply_job_view'),
    path('my-application/',my_application,name='my_application'),
    path('candidate_list_view/<int:id>/',candidate_list_view,name='candidate_list_view'),
]
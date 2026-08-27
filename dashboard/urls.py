from django.urls import path 
from . import views


urlpatterns = [
    path('recruiter_dashboard/',views.recruiter_dashboard,name ='recruiter_dashboard'),
    path('manage-jobs/',views.manage_jobs,name ='manage_jobs'),
    path('applications/',views.recruiter_applications,name ='recruiter_applications'),
    path('applications/<int:app_id>/<str:status>',views.update_application_status,name ='update_application_status'),
    path("analytics/",views.analytics,name="analytics"),
    path('recruiter-profile/',views.recruiter_profile,name='recruiter_profile'),
    path('recruiter-profile/edit',views.edit_recruiter_profile,name='edit_recruiter_profile'),
    
]
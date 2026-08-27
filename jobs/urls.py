from django.urls import path
from . import views

urlpatterns = [
    path('',views.job_list,name ='job_list'),
    path('create/',views.create_job,name='create_job'),
    path('<int:job_id>/',views.job_detail,name='job_detail'),
    path('apply/<int:job_id>/',views.apply_job,name='apply_job'),
    path('my-applications/',views.my_applications,name = 'my_applications'),
    path('edit_job/<int:id>/',views.edit_job,name = 'edit_job'),
    path('delete_job/<int:id>/',views.delete_job,name = 'delete_job'),
    path('apply/<int:id>/',views.apply_job,name = 'apply_job'),
    path('job/<int:job_id>/applications/',views.job_applications,name = 'view_applications'),
    path('shortlist/<int:app_id>/',views.shortlist_application,name = 'shortlist_application'),
    path('reject/<int:app_id>/',views.reject_application,name = 'reject_application'),
    path('questions/<int:job_id>/',views.recruiter_questions,name = 'recruiter_questions'),
    path('feedback/<int:app_id>/',views.add_feedback,name = 'add_feedback'),
    path('ai-feedback/<int:app_id>/',views.ai_feedback,name = 'ai_feedback'),
    path('ai-feedback/<int:app_id>/',views.ai_feedback,name = 'ai_feedback'),
    # path('recruiter/dashboard/',views.recruiter_dashboard,name = 'recruiter_dashboard'),
    path("job/<int:job_id>/applications/",views.job_applications,name="view_applications")
]
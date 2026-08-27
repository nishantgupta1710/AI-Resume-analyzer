from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('upload/',views.upload_resume,name= 'upload_resume'),
    path('analyze/',views.analyze_resume,name= 'analyze_resume'),
    path('mock-interview/',views.mock_interview,name= 'mock_interview'),
    path('career_chatboat/',views.career_chatboat,name= 'career_chatboat'),
    path('cover-leter/',views.cover_letter,name= 'cover_letter'),
    path('resume-loading/',views.resume_loading,name = 'resume_loading')
]


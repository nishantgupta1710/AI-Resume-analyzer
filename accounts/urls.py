from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name= 'home'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup_page,name='signup'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout/',views.logout_page,name='logout'),
    path('dashboard/profile/',views.profile_page,name='profile'),
    path('edit-profile/',views.edit_profile,name='edit_profile')
]
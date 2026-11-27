from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('resumes/', views.resume_list, name='resume-list'),
]

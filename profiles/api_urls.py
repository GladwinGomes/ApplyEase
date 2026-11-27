from django.urls import path
from . import views

app_name = 'profiles-api'

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='api-profile'),
    path('profile/education/', views.EducationListCreateAPIView.as_view(), name='api-education-list'),
    path('profile/education/<int:pk>/', views.EducationDetailAPIView.as_view(), name='api-education-detail'),
    path('profile/experience/', views.ExperienceListCreateAPIView.as_view(), name='api-experience-list'),
    path('profile/experience/<int:pk>/', views.ExperienceDetailAPIView.as_view(), name='api-experience-detail'),
    path('profile/projects/', views.ProjectListCreateAPIView.as_view(), name='api-project-list'),
    path('profile/projects/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='api-project-detail'),
    path('profile/skills/', views.UserSkillListCreateAPIView.as_view(), name='api-skill-list'),
    path('profile/skills/<int:pk>/', views.UserSkillDeleteAPIView.as_view(), name='api-skill-delete'),
    path('resumes/', views.ResumeListCreateAPIView.as_view(), name='api-resume-list'),
    path('resumes/<int:pk>/', views.ResumeDeleteAPIView.as_view(), name='api-resume-delete'),
    path('resumes/<int:pk>/parse/', views.ResumeParseAPIView.as_view(), name='api-resume-parse'),
    path('resumes/<int:pk>/set-default/', views.ResumeSetDefaultAPIView.as_view(), name='api-resume-set-default'),
]

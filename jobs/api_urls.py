from django.urls import path
from . import views

app_name = 'jobs-api'

urlpatterns = [
    path('', views.JobListAPIView.as_view(), name='api-job-list'),
    path('<int:pk>/', views.JobDetailAPIView.as_view(), name='api-job-detail'),
    path('<int:pk>/save/', views.SaveJobAPIView.as_view(), name='api-save-job'),
    path('<int:pk>/unsave/', views.UnsaveJobAPIView.as_view(), name='api-unsave-job'),
    path('saved/', views.SavedJobListAPIView.as_view(), name='api-saved-jobs'),
]

from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Web views
    path('', views.job_list_view, name='job-list'),
    path('<int:pk>/', views.job_detail_view, name='job-detail'),
    path('<int:pk>/save/', views.save_job_view, name='save-job'),
    path('<int:pk>/unsave/', views.unsave_job_view, name='unsave-job'),
    path('saved/', views.saved_jobs_view, name='saved-jobs'),
]

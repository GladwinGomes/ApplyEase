from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('users/', views.user_management_view, name='user-management'),
    path('analytics/', views.analytics_view, name='analytics'),
]

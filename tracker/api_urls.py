from django.urls import path
from . import views

app_name = 'tracker-api'

urlpatterns = [
    path('', views.ApplicationListCreateAPIView.as_view(), name='api-application-list'),
    path('<int:pk>/', views.ApplicationDetailAPIView.as_view(), name='api-application-detail'),
    path('<int:pk>/status/', views.ApplicationStatusUpdateAPIView.as_view(), name='api-application-status'),
    path('kanban/', views.KanbanBoardAPIView.as_view(), name='api-kanban-board'),
    path('reminders/', views.ReminderListCreateAPIView.as_view(), name='api-reminder-list'),
    path('reminders/<int:pk>/', views.ReminderDetailAPIView.as_view(), name='api-reminder-detail'),
]

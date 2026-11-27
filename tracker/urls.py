from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    # Web views
    path('', views.kanban_board_view, name='kanban-board'),
    path('applications/', views.application_list_view, name='application-list'),
    path('applications/create/', views.application_create_view, name='application-create'),
    path('applications/<int:pk>/', views.application_detail_view, name='application-detail'),
    path('applications/<int:pk>/edit/', views.application_edit_view, name='application-edit'),
    path('applications/<int:pk>/delete/', views.application_delete_view, name='application-delete'),
    path('reminders/', views.reminder_list_view, name='reminder-list'),
]

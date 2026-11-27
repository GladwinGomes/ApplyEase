from django.urls import path
from . import views

app_name = 'mock_forms'

urlpatterns = [
    path('form-a/', views.mock_form_a_view, name='form-a'),
    path('form-b/', views.mock_form_b_view, name='form-b'),
    path('form-c/', views.mock_form_c_view, name='form-c'),
]

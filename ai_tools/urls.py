from django.urls import path
from . import views

app_name = 'ai_tools'

urlpatterns = [
    # Web views
    path('match-score/', views.match_score_view, name='match-score'),
    path('cover-letter/', views.cover_letter_view, name='cover-letter'),
    path('match-history/', views.match_history_view, name='match-history'),
]

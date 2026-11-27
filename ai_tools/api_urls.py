from django.urls import path
from . import views

app_name = 'ai_tools-api'

urlpatterns = [
    path('match-score/', views.MatchScoreAPIView.as_view(), name='api-match-score'),
    path('cover-letter/', views.CoverLetterAPIView.as_view(), name='api-cover-letter'),
    path('match-history/', views.MatchHistoryAPIView.as_view(), name='api-match-history'),
]

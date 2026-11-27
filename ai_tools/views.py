from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MatchScore
from .serializers import (
    CoverLetterRequestSerializer,
    MatchScoreRequestSerializer,
    MatchScoreSerializer,
)


# ---------------------------------------------------------------------------
# Web views
# ---------------------------------------------------------------------------


@login_required
def match_score_view(request):
    return render(request, 'ai_tools/match_score.html')


@login_required
def cover_letter_view(request):
    return render(request, 'ai_tools/cover_letter.html')


@login_required
def match_history_view(request):
    scores = MatchScore.objects.filter(user=request.user).select_related('job', 'resume')
    return render(request, 'ai_tools/match_score.html', {'scores': scores})


# ---------------------------------------------------------------------------
# API views
# ---------------------------------------------------------------------------


class MatchScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatchScoreRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': 'Not implemented'},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class CoverLetterAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoverLetterRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': 'Not implemented'},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class MatchHistoryAPIView(generics.ListAPIView):
    serializer_class = MatchScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MatchScore.objects.filter(user=self.request.user).select_related('job', 'resume')

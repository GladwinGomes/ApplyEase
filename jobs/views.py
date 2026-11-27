from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import JobFilter
from .models import Job, SavedJob
from .serializers import JobDetailSerializer, JobListSerializer, SavedJobSerializer


# ---------------------------------------------------------------------------
# Web views
# ---------------------------------------------------------------------------


@login_required
def job_list_view(request):
    jobs = Job.objects.filter(status='active').select_related('company')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(Job.objects.select_related('company'), pk=pk)
    is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'is_saved': is_saved})


@login_required
def save_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.get_or_create(user=request.user, job=job)
    return redirect('jobs:job-detail', pk=pk)


@login_required
def unsave_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    SavedJob.objects.filter(user=request.user, job=job).delete()
    return redirect('jobs:job-detail', pk=pk)


@login_required
def saved_jobs_view(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job__company')
    jobs = [entry.job for entry in saved]
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'saved_only': True})


# ---------------------------------------------------------------------------
# API views
# ---------------------------------------------------------------------------


class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.filter(status='active').select_related('company')
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = JobFilter


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.select_related('company').prefetch_related('job_skills__skill')
    serializer_class = JobDetailSerializer
    permission_classes = [IsAuthenticated]


class SaveJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)
        serializer = SavedJobSerializer(saved_job)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class UnsaveJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        SavedJob.objects.filter(user=request.user, job=job).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedJobListAPIView(generics.ListAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related('job__company')

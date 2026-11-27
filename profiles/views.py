from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Education, Experience, Profile, Project, Resume, UserSkill
from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    ProjectSerializer,
    ResumeSerializer,
    UserSkillSerializer,
)


# ---------------------------------------------------------------------------
# Web views
# ---------------------------------------------------------------------------


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/profile.html', {'profile': profile})


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'profiles/resume_list.html', {'resumes': resumes})


# ---------------------------------------------------------------------------
# API views
# ---------------------------------------------------------------------------


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class EducationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Education.objects.filter(profile=profile)

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class EducationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Education.objects.filter(profile=profile)


class ExperienceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Experience.objects.filter(profile=profile)

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class ExperienceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Experience.objects.filter(profile=profile)


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Project.objects.filter(profile=profile)

    def perform_create(self, serializer):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return Project.objects.filter(profile=profile)


class UserSkillListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user).select_related('skill')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)


class ResumeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class ResumeParseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        return Response(
            {'detail': 'Not implemented'},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class ResumeSetDefaultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        Resume.objects.filter(user=request.user, is_default=True).update(is_default=False)
        resume.is_default = True
        resume.save(update_fields=['is_default'])
        return Response(ResumeSerializer(resume).data, status=status.HTTP_200_OK)

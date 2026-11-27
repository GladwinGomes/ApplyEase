from rest_framework import serializers

from core.models import Skill
from .models import Education, Experience, Profile, Project, Resume, UserSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name', 'category']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'profile',
            'institution',
            'degree',
            'field_of_study',
            'start_year',
            'end_year',
            'grade',
        ]
        read_only_fields = ['id', 'profile']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'profile',
            'company_name',
            'job_title',
            'start_date',
            'end_date',
            'description',
        ]
        read_only_fields = ['id', 'profile']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'profile',
            'title',
            'description',
            'tech_stack',
            'url',
        ]
        read_only_fields = ['id', 'profile']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'id',
            'user',
            'file_name',
            'file_path',
            'parsed_text',
            'is_default',
            'uploaded_at',
        ]
        read_only_fields = ['id', 'user', 'parsed_text', 'uploaded_at']


class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.skill_name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'skill_name', 'category', 'proficiency']
        read_only_fields = ['id', 'user']


class ProfileSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'email',
            'phone',
            'location',
            'linkedin_url',
            'github_url',
            'portfolio_url',
            'summary',
            'educations',
            'experiences',
            'projects',
        ]
        read_only_fields = ['id', 'user']

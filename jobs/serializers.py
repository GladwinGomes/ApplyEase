from rest_framework import serializers

from .models import Company, Job, JobSkill, SavedJob


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'website', 'industry', 'logo_url']


class JobSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.skill_name', read_only=True)
    category = serializers.CharField(source='skill.category', read_only=True)

    class Meta:
        model = JobSkill
        fields = ['id', 'skill', 'skill_name', 'category']


class JobListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    company_logo = serializers.URLField(source='company.logo_url', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company',
            'company_name',
            'company_logo',
            'location',
            'job_type',
            'work_mode',
            'posted_date',
            'status',
        ]


class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    job_skills = JobSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'company',
            'title',
            'description',
            'location',
            'job_type',
            'work_mode',
            'apply_url',
            'posted_date',
            'status',
            'job_skills',
        ]


class SavedJobSerializer(serializers.ModelSerializer):
    job = JobListSerializer(read_only=True)

    class Meta:
        model = SavedJob
        fields = ['id', 'user', 'job', 'saved_at']
        read_only_fields = ['id', 'user', 'saved_at']

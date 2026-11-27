from rest_framework import serializers

from .models import CoverLetter, MatchScore


class MatchScoreSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    resume_name = serializers.CharField(source='resume.file_name', read_only=True)

    class Meta:
        model = MatchScore
        fields = [
            'id',
            'user',
            'job',
            'job_title',
            'resume',
            'resume_name',
            'score',
            'missing_keywords',
            'generated_at',
        ]
        read_only_fields = ['id', 'user', 'score', 'missing_keywords', 'generated_at']


class MatchScoreRequestSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    resume_id = serializers.IntegerField()


class CoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverLetter
        fields = ['id', 'application', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class CoverLetterRequestSerializer(serializers.Serializer):
    application_id = serializers.IntegerField()
    tone = serializers.ChoiceField(
        choices=['professional', 'enthusiastic', 'concise'],
        default='professional',
        required=False,
    )
    additional_notes = serializers.CharField(required=False, allow_blank=True)

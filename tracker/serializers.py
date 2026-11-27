from rest_framework import serializers

from jobs.serializers import JobListSerializer
from .models import Application, Reminder, StatusLog


class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = ['id', 'application', 'old_status', 'new_status', 'changed_at']
        read_only_fields = ['id', 'changed_at']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'application', 'remind_on', 'message', 'is_sent']
        read_only_fields = ['id', 'is_sent']


class ApplicationSerializer(serializers.ModelSerializer):
    job_detail = JobListSerializer(source='job', read_only=True)
    status_logs = StatusLogSerializer(many=True, read_only=True)
    reminders = ReminderSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'job',
            'job_detail',
            'resume',
            'status',
            'applied_date',
            'notes',
            'external_url',
            'status_logs',
            'reminders',
        ]
        read_only_fields = ['id', 'user']


class KanbanBoardSerializer(serializers.Serializer):
    saved = ApplicationSerializer(many=True, read_only=True)
    applied = ApplicationSerializer(many=True, read_only=True)
    interview = ApplicationSerializer(many=True, read_only=True)
    offer = ApplicationSerializer(many=True, read_only=True)
    rejected = ApplicationSerializer(many=True, read_only=True)

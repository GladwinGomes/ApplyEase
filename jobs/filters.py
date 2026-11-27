import django_filters
from django.db.models import Q

from .models import Job


class JobFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    job_type = django_filters.ChoiceFilter(choices=Job.JOB_TYPE_CHOICES)
    work_mode = django_filters.ChoiceFilter(choices=Job.WORK_MODE_CHOICES)
    skills = django_filters.CharFilter(method='filter_skills', label='Skills')

    class Meta:
        model = Job
        fields = ['location', 'job_type', 'work_mode', 'status']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )

    def filter_skills(self, queryset, name, value):
        skill_names = [s.strip() for s in value.split(',') if s.strip()]
        if not skill_names:
            return queryset
        return queryset.filter(
            job_skills__skill__skill_name__in=skill_names
        ).distinct()

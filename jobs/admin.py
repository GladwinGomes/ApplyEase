from django.contrib import admin

from .models import Company, Job, JobSkill, SavedJob


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'industry', 'website')
    search_fields = ('company_name', 'industry')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'work_mode', 'status', 'posted_date')
    list_filter = ('job_type', 'work_mode', 'status')
    search_fields = ('title', 'description', 'company__company_name', 'location')


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('job', 'skill')
    search_fields = ('job__title', 'skill__skill_name')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__email', 'job__title')

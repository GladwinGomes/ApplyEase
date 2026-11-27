from django.contrib import admin

from .models import Education, Experience, Profile, Project, Resume, UserSkill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location')
    search_fields = ('user__email', 'location')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'institution', 'degree', 'start_year', 'end_year')
    search_fields = ('institution', 'degree', 'field_of_study')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('company_name', 'job_title')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'tech_stack')
    search_fields = ('title', 'tech_stack')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'is_default', 'uploaded_at')
    list_filter = ('is_default',)
    search_fields = ('file_name', 'user__email')


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency')
    list_filter = ('proficiency',)
    search_fields = ('user__email', 'skill__skill_name')

from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'category')
    list_filter = ('category',)
    search_fields = ('skill_name', 'category')

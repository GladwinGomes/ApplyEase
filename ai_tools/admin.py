from django.contrib import admin

from .models import CoverLetter, MatchScore


@admin.register(MatchScore)
class MatchScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'resume', 'score', 'generated_at')
    search_fields = ('user__email', 'job__title')


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ('application', 'created_at')

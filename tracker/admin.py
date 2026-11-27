from django.contrib import admin

from .models import Application, Reminder, StatusLog


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_date')
    list_filter = ('status',)
    search_fields = ('user__email', 'job__title')


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('application', 'old_status', 'new_status', 'changed_at')
    list_filter = ('new_status',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('application', 'remind_on', 'is_sent')
    list_filter = ('is_sent',)

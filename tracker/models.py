from django.conf import settings
from django.db import models


class Application(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications',
    )
    resume = models.ForeignKey(
        'profiles.Resume',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='saved',
    )
    applied_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    external_url = models.URLField(
        null=True, blank=True, help_text="Link to the external application"
    )

    class Meta:
        db_table = 'applications'
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.user} — {self.job} ({self.status})"


class StatusLog(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='status_logs',
    )
    old_status = models.CharField(
        max_length=15,
        choices=Application.STATUS_CHOICES,
        null=True,
        blank=True,
    )
    new_status = models.CharField(
        max_length=15,
        choices=Application.STATUS_CHOICES,
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'status_logs'
        ordering = ['-changed_at']

    def __str__(self):
        return f"Application #{self.application_id}: {self.old_status} → {self.new_status}"


class Reminder(models.Model):
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='reminders',
    )
    remind_on = models.DateTimeField()
    message = models.CharField(max_length=300, blank=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'reminders'
        ordering = ['remind_on']

    def __str__(self):
        return f"Reminder for Application #{self.application_id} on {self.remind_on}"

from django.conf import settings
from django.db import models


class MatchScore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='match_scores',
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='match_scores',
    )
    resume = models.ForeignKey(
        'profiles.Resume',
        on_delete=models.CASCADE,
        related_name='match_scores',
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Resume-to-job match score (0–100)",
    )
    missing_keywords = models.JSONField(
        null=True,
        blank=True,
        help_text="List of keywords missing from the resume",
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_scores'
        ordering = ['-generated_at']

    def __str__(self):
        return f"Match {self.score}% — {self.user} vs {self.job}"


class CoverLetter(models.Model):
    application = models.ForeignKey(
        'tracker.Application',
        on_delete=models.CASCADE,
        related_name='cover_letters',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cover_letters'
        ordering = ['-created_at']

    def __str__(self):
        return f"Cover letter for Application #{self.application_id}"

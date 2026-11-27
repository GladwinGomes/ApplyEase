from django.conf import settings
from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.company_name


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    WORK_MODE_CHOICES = [
        ('on-site', 'On-Site'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=150, blank=True, null=True)
    job_type = models.CharField(
        max_length=15,
        choices=JOB_TYPE_CHOICES,
        help_text="Type of employment",
    )
    work_mode = models.CharField(
        max_length=10,
        choices=WORK_MODE_CHOICES,
        default='on-site',
    )
    apply_url = models.URLField(blank=True, null=True, help_text="External application URL")
    posted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )

    class Meta:
        db_table = 'jobs'
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobSkill(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_skills',
    )
    skill = models.ForeignKey(
        'core.Skill',
        on_delete=models.CASCADE,
        related_name='job_skills',
    )

    class Meta:
        db_table = 'job_skills'
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.job.title} — {self.skill}"


class SavedJob(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_jobs',
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='saved_by',
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_jobs'
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user} saved {self.job}"

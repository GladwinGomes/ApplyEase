from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    linkedin_url = models.URLField(
        blank=True, null=True, help_text="LinkedIn profile URL"
    )
    github_url = models.URLField(
        blank=True, null=True, help_text="GitHub profile URL"
    )
    portfolio_url = models.URLField(
        blank=True, null=True, help_text="Personal portfolio URL"
    )
    summary = models.TextField(
        blank=True, null=True, help_text="Brief professional summary"
    )

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f"Profile of {self.user}"


class Education(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='educations',
    )
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=150, blank=True, null=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True, null=True)
    grade = models.CharField(
        max_length=20, blank=True, null=True, help_text="e.g., 3.8 GPA, First Class"
    )

    class Meta:
        db_table = 'education'
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='experiences',
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True, null=True, help_text="Leave blank if this is your current role"
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'experience'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Project(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tech_stack = models.CharField(
        max_length=300, blank=True, null=True, help_text="Comma-separated technologies"
    )
    url = models.URLField(blank=True, null=True, help_text="Project or repo URL")

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.title


class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
    )
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='resumes/')
    parsed_text = models.TextField(
        blank=True, null=True, help_text="Extracted text from the resume"
    )
    is_default = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resumes'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.file_name} ({self.user})"


class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_skills',
    )
    skill = models.ForeignKey(
        'core.Skill',
        on_delete=models.CASCADE,
        related_name='user_skills',
    )
    proficiency = models.CharField(
        max_length=15,
        choices=PROFICIENCY_CHOICES,
        default='intermediate',
    )

    class Meta:
        db_table = 'user_skills'
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} — {self.skill} ({self.proficiency})"

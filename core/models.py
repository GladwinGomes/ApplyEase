from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g., language, framework, tool",
    )

    class Meta:
        db_table = 'skills'
        ordering = ['skill_name']

    def __str__(self):
        return self.skill_name

"""Résumés and job descriptions saved by one account.

An analysis row is the link between one résumé and one description.
Nothing fills that row in yet. There is no model call here.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

# A paste, not a document upload. Long enough for a full description,
# short enough that one request cannot fill the disk.
PASTE_MAX_LENGTH = 100_000


class Resume(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(validators=[MaxLengthValidator(PASTE_MAX_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return self.title or f"Résumé {self.pk}"


class JobDescription(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_descriptions",
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    text = models.TextField(validators=[MaxLengthValidator(PASTE_MAX_LENGTH)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return f"{self.company} · {self.role}"


class Analysis(models.Model):
    """One résumé compared with one job description.

    The row is stored so a later change can fill in a result. This
    model does not call a model and does not extract skills.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["resume", "job_description"],
                name="unique_analysis_per_resume_and_description",
            )
        ]

    def __str__(self) -> str:
        return f"Analysis {self.pk}"

    def save(self, *args: object, **kwargs: object) -> None:
        """Refuse a résumé or description owned by a different account.

        create() and save() both come through here. QuerySet.update()
        does not, and this app has no view that updates an analysis.
        """
        errors = {}
        if self.resume.owner_id != self.owner_id:
            errors["resume"] = "That résumé belongs to another account."
        if self.job_description.owner_id != self.owner_id:
            errors["job_description"] = "That description belongs to another account."
        if errors:
            raise ValidationError(errors)
        super().save(*args, **kwargs)

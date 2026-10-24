from django.db import models
from django.contrib.auth.models import User
from applications.models import Application


class Interview(models.Model):

    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    interview_type = models.CharField(
        max_length=50,
        default="Online"
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Interview - Application #{self.application.id}"
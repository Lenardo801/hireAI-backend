from django.db import models
from django.contrib.auth.models import User


# Job Model
class Job(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=500)
    experience = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # Job reminder field
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Application Model
class Application(models.Model):
    STATUS_CHOICES = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
        ("interview", "Interview"),
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )
    ai_score = models.FloatField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"


# Interview Model
class Interview(models.Model):
    INTERVIEW_TYPE_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
    )

    STATUS_CHOICES = (
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="interviews"
    )
    interview_date = models.DateField()
    interview_time = models.TimeField()
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default="online"
    )
    meeting_link = models.URLField(
        blank=True,
        null=True
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Interview Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )

    # Interview reminder field
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Interview - Application #{self.application.id}"
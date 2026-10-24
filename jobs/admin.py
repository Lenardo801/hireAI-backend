from django.contrib import admin

from .models import Job, Application, Interview


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "company",
        "location",
        "recruiter",
        "experience",
        "created_at",
    )

    list_filter = (
        "location",
        "experience",
        "created_at",
    )

    search_fields = (
        "title",
        "company",
        "location",
        "skills",
        "description",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "candidate",
        "job",
        "ai_score",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "candidate__username",
        "candidate__email",
        "job__title",
        "job__company",
    )

    ordering = (
        "-applied_at",
    )


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "application",
        "interview_date",
        "interview_time",
        "interview_type",
        "created_at",
    )

    list_filter = (
        "interview_type",
        "interview_date",
    )

    search_fields = (
        "application__candidate__username",
        "application__candidate__email",
        "application__job__title",
    )

    ordering = (
        "interview_date",
        "interview_time",
    )

from rest_framework import serializers

from .models import Job, Application, Interview


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job

        fields = [
            "id",
            "recruiter",
            "title",
            "company",
            "location",
            "description",
            "skills",
            "experience",
            "created_at",
        ]


class ApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    job_company = serializers.CharField(
        source="job.company",
        read_only=True
    )

    job_location = serializers.CharField(
        source="job.location",
        read_only=True
    )

    class Meta:
        model = Application

        fields = [
            "id",
            "candidate",
            "job",

            "job_title",
            "job_company",
            "job_location",

            "resume",
            "ai_score",
            "status",
            "applied_at",
        ]

        read_only_fields = [
            "ai_score",
            "status",
            "applied_at",
            "job_title",
            "job_company",
            "job_location",
        ]


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            "id",
            "application",
            "interview_date",
            "interview_time",
            "interview_type",
            "meeting_link",
            "location",
            "notes",
            "status",
            "created_at",
        ]

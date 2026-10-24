from rest_framework import serializers

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):

    class Meta:

        model = Interview

        fields = [
            "id",
            "application",
            "recruiter",
            "interview_date",
            "interview_time",
            "interview_type",
            "meeting_link",
            "status",
            "created_at",
        ]
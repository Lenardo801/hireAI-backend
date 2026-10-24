from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from pypdf import PdfReader

from .models import Application
from .serializers import ApplicationSerializer


def calculate_ai_score(resume_file, job):

    reader = PdfReader(resume_file)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text.lower()

    job_skills = job.skills.lower().split(",")

    matched_skills = 0

    for skill in job_skills:

        skill = skill.strip()

        if skill and skill in resume_text:
            matched_skills += 1

    if len(job_skills) == 0:
        return 0

    score = (matched_skills / len(job_skills)) * 100

    return round(score, 2)


class ApplicationListCreateView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):

        applications = Application.objects.all().order_by("-applied_at")

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = ApplicationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            application = serializer.save()

            score = calculate_ai_score(
                application.resume,
                application.job
            )

            application.ai_score = score
            application.save()

            return Response(
                {
                    "message": "Application submitted successfully",
                    "ai_score": score,
                    "application": ApplicationSerializer(
                        application
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ApplicationStatusUpdateView(APIView):

    def patch(self, request, application_id):

        try:

            application = Application.objects.get(
                id=application_id
            )

        except Application.DoesNotExist:

            return Response(
                {"message": "Application not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")

        allowed_statuses = [
            "applied",
            "shortlisted",
            "rejected",
            "interview",
            "selected",
        ]

        if new_status not in allowed_statuses:

            return Response(
                {"message": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status
        application.save()

        return Response(
            {
                "message": "Application status updated successfully",
                "application": ApplicationSerializer(
                    application
                ).data
            }
        )
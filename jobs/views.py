from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User 
from rest_framework.decorators import api_view
from rest_framework.response import Response


from pypdf import PdfReader

from .models import Job, Application, Interview

from .serializers import (
    JobSerializer,
    ApplicationSerializer,
    InterviewSerializer,
)

from notifications.models import Notification




# =========================================================
# RESUME TEXT EXTRACTION
# =========================================================

def extract_resume_text(resume_file):

    reader = PdfReader(resume_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================================
# AI RESUME MATCHING
# =========================================================

def calculate_ai_score(resume_text, job_skills):

    resume_text = resume_text.lower()

    skills = [
        skill.strip().lower()
        for skill in job_skills.split(",")
        if skill.strip()
    ]

    if not skills:

        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in resume_text:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    score = (
        len(matched_skills) / len(skills)
    ) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


# =========================================================
# JOB LIST + CREATE
# =========================================================

class JobListCreateView(APIView):

    def get(self, request):

        jobs = Job.objects.all().order_by(
            "-created_at"
        )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = JobSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Job created successfully",
                    "job": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# APPLY FOR JOB + AI SCORE
# =========================================================

class ApplicationCreateView(APIView):

    def post(self, request):

        serializer = ApplicationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            application = serializer.save()

            resume_text = ""

            if application.resume:

                try:

                    resume_text = extract_resume_text(
                        application.resume
                    )

                except Exception as error:

                    print(
                        "Resume extraction error:",
                        error
                    )

            job = application.job

            ai_result = calculate_ai_score(
                resume_text,
                job.skills
            )

            score = ai_result["score"]

            application.ai_score = score

            application.save()

            return Response(
                {
                    "message": (
                        "Application submitted successfully"
                    ),

                    "ai_score": score,

                    "matched_skills":
                        ai_result["matched_skills"],

                    "missing_skills":
                        ai_result["missing_skills"],

                    "application":
                        ApplicationSerializer(
                            application
                        ).data,
                },

                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# APPLICATION LIST
# =========================================================

class ApplicationListView(APIView):

    def get(self, request):

        candidate_id = request.GET.get(
            "candidate"
        )

        job_id = request.GET.get(
            "job"
        )

        if candidate_id:

            applications = Application.objects.filter(
                candidate_id=candidate_id
            ).order_by(
                "-applied_at"
            )

        elif job_id:

            applications = Application.objects.filter(
                job_id=job_id
            ).order_by(
                "-applied_at"
            )

        else:

            applications = Application.objects.all().order_by(
                "-applied_at"
            )

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(
            serializer.data
        )


# =========================================================
# APPLICATION STATUS UPDATE
# =========================================================

class ApplicationStatusUpdateView(APIView):

    def patch(self, request, application_id):

        try:

            application = Application.objects.get(
                id=application_id
            )

        except Application.DoesNotExist:

            return Response(
                {
                    "error": "Application not found"
                },
                status=404
            )

        new_status = request.data.get(
            "status"
        )

        allowed_statuses = [
            "applied",
            "shortlisted",
            "rejected",
            "selected",
            "interview",
        ]

        if new_status not in allowed_statuses:

            return Response(
                {
                    "error": "Invalid status"
                },
                status=400
            )

        # =================================================
        # UPDATE APPLICATION STATUS
        # =================================================

        application.status = new_status

        application.save()

        # =================================================
        # SHORTLISTED NOTIFICATION
        # =================================================

        if new_status == "shortlisted":

            already_notified = Notification.objects.filter(
                user=application.candidate,
                title="Application Shortlisted ⭐",
                message__icontains=application.job.title,
            ).exists()

            if not already_notified:

                Notification.objects.create(

                    user=application.candidate,

                    title="Application Shortlisted ⭐",

                    message=(
                        f"Congratulations! Your application "
                        f"for {application.job.title} at "
                        f"{application.job.company} "
                        f"has been shortlisted."
                    ),

                    notification_type="application"
                )

        # =================================================
        # REJECTED NOTIFICATION
        # =================================================

        elif new_status == "rejected":

            already_notified = Notification.objects.filter(
                user=application.candidate,
                title="Application Update",
                message__icontains=application.job.title,
            ).exists()

            if not already_notified:

                Notification.objects.create(

                    user=application.candidate,

                    title="Application Update",

                    message=(
                        f"Your application for "
                        f"{application.job.title} at "
                        f"{application.job.company} "
                        f"was not selected at this time."
                    ),

                    notification_type="application"
                )

        # =================================================
        # INTERVIEW STATUS NOTIFICATION
        # =================================================

        elif new_status == "interview":

            already_notified = Notification.objects.filter(
                user=application.candidate,
                title="Interview Update 📅",
                message__icontains=application.job.title,
            ).exists()

            if not already_notified:

                Notification.objects.create(

                    user=application.candidate,

                    title="Interview Update 📅",

                    message=(
                        f"Your application for "
                        f"{application.job.title} at "
                        f"{application.job.company} "
                        f"has moved to the interview stage."
                    ),

                    notification_type="interview"
                )

        # =================================================
        # RETURN UPDATED APPLICATION
        # =================================================

        serializer = ApplicationSerializer(
            application
        )

        return Response(
            {
                "message":
                    "Application status updated successfully",

                "application":
                    serializer.data,
            }
        )


# =========================================================
# CREATE INTERVIEW
# =========================================================

class InterviewCreateView(APIView):

    def post(self, request):

        application_id = request.data.get(
            "application"
        )

        # =================================================
        # DUPLICATE INTERVIEW CHECK
        # =================================================

        if Interview.objects.filter(
            application_id=application_id
        ).exists():

            return Response(
                {
                    "error": (
                        "Interview already scheduled "
                        "for this application"
                    )
                },
                status=400
            )

        serializer = InterviewSerializer(
            data=request.data
        )

        if serializer.is_valid():

            interview = serializer.save()

            application = interview.application

            # =================================================
            # UPDATE APPLICATION STATUS
            # =================================================

            application.status = "interview"

            application.save()

            # =================================================
            # INTERVIEW NOTIFICATION
            # =================================================

            Notification.objects.create(

                user=application.candidate,

                title="Interview Scheduled 📅",

                message=(
                    f"Your interview for {application.job.title} "
                    f"at {application.job.company} has been scheduled "
                    f"on {interview.interview_date} "
                    f"at {interview.interview_time}."
                ),

                notification_type="interview"
            )

            return Response(
                {
                    "message":
                        "Interview scheduled successfully",

                    "interview":
                        InterviewSerializer(
                            interview
                        ).data,
                },

                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


# =========================================================
# INTERVIEW LIST
# =========================================================

class InterviewListView(APIView):

    def get(self, request):

        candidate_id = request.GET.get(
            "candidate"
        )

        if candidate_id:

            interviews = Interview.objects.filter(
                application__candidate_id=candidate_id
            ).order_by(
                "interview_date",
                "interview_time"
            )

        else:

            interviews = Interview.objects.all().order_by(
                "interview_date",
                "interview_time"
            )

        serializer = InterviewSerializer(
            interviews,
            many=True
        )

        return Response(
            serializer.data
        )


# =========================================================
# UPDATE EXISTING INTERVIEW
# =========================================================

class InterviewUpdateView(APIView):
    def patch(self, request, interview_id):
        try:
            interview = Interview.objects.select_related(
                "application__job"
            ).get(id=interview_id)
        except Interview.DoesNotExist:
            return Response(
                {"error": "Interview not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check whether the recruiter owns this job
        recruiter_id = request.data.get("recruiter_id")

        if not recruiter_id:
            return Response(
                {"error": "Recruiter ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if interview.application.job.recruiter_id != int(recruiter_id):
            return Response(
                {"error": "You cannot update this interview"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = InterviewSerializer(
            interview,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Interview updated successfully",
                "interview": serializer.data
            })

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def admin_analytics_view(request):
    total_users = User.objects.count()

    total_recruiters = User.objects.filter(
        profile__role='recruiter'
    ).count()

    total_jobs = Job.objects.count()

    total_applications = Application.objects.count()

    data = {
        "total_users": total_users,
        "total_recruiters": total_recruiters,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
    }

    return Response(data)
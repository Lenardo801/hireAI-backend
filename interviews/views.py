from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Interview
from .serializers import InterviewSerializer


# =========================================================
# INTERVIEW LIST AND CREATE
# =========================================================

class InterviewListCreateView(APIView):

    # GET: List interviews
    def get(self, request):

        candidate_id = request.query_params.get("candidate")

        interviews = Interview.objects.all()

        # Filter interviews for the logged-in candidate
        if candidate_id:
            interviews = interviews.filter(
                application__candidate_id=candidate_id
            )

        # Sort interviews by date and time
        interviews = interviews.order_by(
            "interview_date",
            "interview_time"
        )

        serializer = InterviewSerializer(
            interviews,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST: Schedule an interview
    def post(self, request):

        serializer = InterviewSerializer(
            data=request.data
        )

        if serializer.is_valid():

            interview = serializer.save()

            return Response(
                {
                    "message": "Interview scheduled successfully",
                    "interview": InterviewSerializer(
                        interview
                    ).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# INTERVIEW STATUS UPDATE
# =========================================================

class InterviewStatusUpdateView(APIView):

    # PATCH: Update interview status
    def patch(self, request, interview_id):

        try:
            interview = Interview.objects.get(
                id=interview_id
            )

        except Interview.DoesNotExist:

            return Response(
                {
                    "message": "Interview not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")

        allowed_statuses = [
            "scheduled",
            "completed",
            "cancelled"
        ]

        if new_status not in allowed_statuses:

            return Response(
                {
                    "message": "Invalid interview status"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        interview.status = new_status
        interview.save()

        return Response(
            {
                "message": "Interview status updated successfully",
                "interview": InterviewSerializer(
                    interview
                ).data
            },
            status=status.HTTP_200_OK
        )
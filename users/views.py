from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from django.contrib.auth import authenticate

from .serializers import RegisterSerializer
from .models import Profile


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            profile = Profile.objects.get(
                user=user
            )

            return Response(
                {
                    "message": "Registration successful",
                    "username": user.username,
                    "email": user.email,
                    "role": profile.role,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:

            return Response(
                {
                    "message": "Username and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:

            return Response(
                {
                    "message": "Invalid username or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:

            profile = Profile.objects.get(
                user=user
            )

        except Profile.DoesNotExist:

            return Response(
                {
                    "message": "User profile not found"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Login successful",
                "username": user.username,
                "email": user.email,
                "role": profile.role,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK
        )


class AdminUsersView(APIView):
    def get(self, request):
        users = User.objects.all().order_by("-date_joined")

        data = []

        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                role = profile.role
            except Profile.DoesNotExist:
                role = "candidate"

            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": role,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
            })

        return Response(data, status=status.HTTP_200_OK)


class AdminRecruitersView(APIView):
    def get(self, request):
        recruiters = Profile.objects.filter(
            role="recruiter"
        ).select_related("user").order_by("-user__date_joined")

        data = []

        for profile in recruiters:
            user = profile.user

            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": profile.role,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
            })

        return Response(data, status=status.HTTP_200_OK)
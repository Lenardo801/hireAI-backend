from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Notification


class NotificationListView(APIView):
    def get(self, request):
        user_id = request.GET.get("user")

        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notifications = Notification.objects.filter(
            user_id=user_id
        ).order_by("-created_at")

        data = [
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]

        return Response(data)


class NotificationReadView(APIView):
    def patch(self, request, notification_id):
        user_id = request.GET.get("user")

        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            notification = Notification.objects.get(
                id=notification_id,
                user_id=user_id,
            )
        except Notification.DoesNotExist:
            return Response(
                {"error": "Notification not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response({
            "message": "Notification marked as read"
        })
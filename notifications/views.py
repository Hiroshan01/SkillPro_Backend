from django.db import models
from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer


class MyNotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        role = getattr(self.request.user, "role", "")
        return Notification.objects.filter(
            models.Q(target_role__icontains=role) | models.Q(target_role="")
        ).order_by("-created_at")


# Admin/instructor: create notification
class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Restrict further in production

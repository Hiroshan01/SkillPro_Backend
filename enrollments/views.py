from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from .models import Enrollment
from .serializers import EnrollmentSerializer


class StudentEnrollmentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "student":
            return Enrollment.objects.filter(student=user)
        elif user.role in ["admin", "instructor"]:
            return Enrollment.objects.all()
        return Enrollment.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save(student=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "You are already enrolled in this course."})


class CourseEnrollmentListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Enrollment.objects.filter(course__id=course_id)
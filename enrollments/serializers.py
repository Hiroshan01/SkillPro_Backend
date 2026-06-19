from courses.models import Course
from rest_framework import serializers
from users.models import User

from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.name", read_only=True)
    student_name = serializers.SerializerMethodField()
    course = serializers.SlugRelatedField(
        slug_field="name", queryset=Course.objects.all()
    )
    student = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "student",
            "student_name",
            "course",
            "course_name",
            "registered_on",
            "status",
            "certificate_issued",
        ]

    def get_student_name(self, obj):
        """Get full name of the student"""
        if obj.student.first_name and obj.student.last_name:
            return f"{obj.student.first_name} {obj.student.last_name}"
        return obj.student.get_full_name() or obj.student.username

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_staff:
            validated_data["student"] = request.user
        return super().create(validated_data)

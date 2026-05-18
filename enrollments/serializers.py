from courses.models import Course
from rest_framework import serializers
from users.models import User

from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
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
            "course",
            "registered_on",
            "status",
            "certificate_issued",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_staff:
            validated_data["student"] = request.user
        return super().create(validated_data)
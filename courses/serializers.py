from rest_framework import serializers
from users.models import User

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructors = serializers.SlugRelatedField(
        slug_field="username",
        many=True,
        queryset=User.objects.filter(role="instructor"),
    )

    class Meta:
        model = Course
        fields = "__all__"

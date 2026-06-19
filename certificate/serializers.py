from rest_framework import serializers

from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id",
            "certificate_number",
            "student",
            "student_name",
            "course",
            "course_name",
            "enrollment",
            "issue_date",
            "expiry_date",
            "status",
            "grade",
            "certificate_file",
            "notes",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "certificate_number",
            "issue_date",
            "created_at",
            "student_name",
            "course_name",
        ]

from django.urls import path
from .views import StudentEnrollmentListCreateAPIView, CourseEnrollmentListAPIView

urlpatterns = [
    path('', StudentEnrollmentListCreateAPIView.as_view(), name='my-enrollments'),  # /api/enrollments/
    path('course/<int:course_id>/', CourseEnrollmentListAPIView.as_view(), name='course-enrollments'),  # /api/enrollments/course/1/
]
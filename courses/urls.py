from django.urls import path

from .views import CourseListCreateAPI, CourseRetrieveUpdateAPI

urlpatterns = [
    path("register/", CourseListCreateAPI.as_view(), name="course-list-create"),
    path("<int:pk>/", CourseRetrieveUpdateAPI.as_view(), name="course-detail-update"),
]

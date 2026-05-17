from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes for new apps
    path("api/users/", include("users.urls"), name="users"),
    path("api/courses/", include("courses.urls"), name="courses"),
    path("api/enrollments/", include("enrollments.urls"), name="enrollments"),
    path("api/events/", include("events.urls"), name="events"),
    path("api/inquiries/", include("inquiries.urls"), name="inquiries"),
    path("api/notifications/", include("notifications.urls"), name="notifications"),
]
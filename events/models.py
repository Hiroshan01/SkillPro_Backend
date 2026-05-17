from django.db import models
from courses.models import Course

class Event(models.Model):
    EVENT_TYPES = [
        ("batch", "Batch"),
        ("holiday", "Holiday"),
        ("seminar", "Seminar"),
        ("jobfair", "Job Fair"),
        ("exam", "Exam"),
        ("workshop", "Workshop"),
        # Add more as needed
    ]
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")  # Optional: event can be course-specific

    def __str__(self):
        return f"{self.title} ({self.event_type})"
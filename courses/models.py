from django.db import models
from users.models import User


class Course(models.Model):
    CATEGORY_CHOICES = [
        ("ICT", "ICT"),
        ("Plumbing", "Plumbing"),
        ("Welding", "Welding"),
        ("Hotel Management", "Hotel Management"),
        # Add more categories as needed
    ]
    MODE_CHOICES = [
        ("online", "Online"),
        ("onsite", "On-site"),
    ]

    LOCATION_CHOICES = [
        ("Colombo", "Colombo"),
        ("Kandy", "Kandy"),
        ("Matara", "Matara"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    location = models.CharField(
        max_length=100, choices=LOCATION_CHOICES
    )  # "Colombo", "Kandy", etc, or "Online"
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    duration_weeks = models.IntegerField()
    instructors = models.ManyToManyField(
        User, related_name="courses", limit_choices_to={"role": "instructor"}
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.category}"

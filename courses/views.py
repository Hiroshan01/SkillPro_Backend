from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPI(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # anyone can list, auth needed to create

class CourseRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


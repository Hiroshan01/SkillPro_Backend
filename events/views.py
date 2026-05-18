from rest_framework import generics, permissions

from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            user = self.request.user
            if user and user.is_authenticated and user.role in ["admin", "instructor"]:
                return [IsAuthenticated()]
            return [permissions.IsAdminUser()]  
        return [permissions.AllowAny()]


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

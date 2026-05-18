from rest_framework import generics, permissions

from .models import Inquiry
from .permissions import IsAdminOrInstructor
from .serializers import InquirySerializer


class InquiryCreateAPIView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]  # Anyone can submit

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class InquiryListAPIView(generics.ListAPIView):
    queryset = Inquiry.objects.all().order_by("-created_at")
    serializer_class = InquirySerializer
    permission_classes = [IsAdminOrInstructor]

from django.urls import path

from .views import InquiryCreateAPIView, InquiryListAPIView

urlpatterns = [
    path(
        "", InquiryCreateAPIView.as_view(), name="inquiry-create"
    ), 
    path(
        "all/", InquiryListAPIView.as_view(), name="inquiry-list"
    ),
]

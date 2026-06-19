from django.urls import path
from .views import (
    MyCertificatesListView,
    CertificateDetailView,
    CertificateCreateView,
    CertificateUpdateView,
    CertificateListView,
    issue_certificate,
)

urlpatterns = [
    # Student: Get their certificates
    path('my-certificates/', MyCertificatesListView.as_view(), name='my-certificates'),
    
    # Student: Get single certificate
    path('<int:pk>/', CertificateDetailView.as_view(), name='certificate-detail'),
    
    # Admin/Instructor: Create certificate
    path('create/', CertificateCreateView.as_view(), name='certificate-create'),
    
    # Admin/Instructor: Update certificate
    path('<int:pk>/update/', CertificateUpdateView.as_view(), name='certificate-update'),
    
    # Admin/Instructor: List all certificates
    path('list-all/', CertificateListView.as_view(), name='certificate-list-all'),
    
    # Admin/Instructor: Issue certificate
    path('<int:pk>/issue/', issue_certificate, name='issue-certificate'),
]
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Certificate
from .serializers import CertificateSerializer
from enrollments.models import Enrollment
from django.db import transaction

# Student: Get their certificates
class MyCertificatesListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)


# Student: Get single certificate details
class CertificateDetailView(generics.RetrieveAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Certificate.objects.all()

    def get_queryset(self):
        # Students can only see their own certificates
        if self.request.user.role == 'student':
            return Certificate.objects.filter(student=self.request.user)
        # Admin/Instructor can see all
        return Certificate.objects.all()


# Admin/Instructor: Create certificate for student
class CertificateCreateView(generics.CreateAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        
        # Only admin/instructor can create certificates
        if user.role not in ['admin', 'instructor']:
            return Response(
                {'error': 'Only admin or instructor can create certificates.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            with transaction.atomic():  # <-- Add atomic transaction
                enrollment_id = request.data.get('enrollment')
                enrollment = Enrollment.objects.get(id=enrollment_id)
                
                # Generate unique certificate number
                year = 2026
                count = Certificate.objects.filter(
                    created_at__year=year
                ).count() + 1
                cert_number = f"CERT-{year}-{count:05d}"
                
                certificate_data = {
                    'enrollment': enrollment.id,
                    'student': enrollment.student.id,
                    'course': enrollment.course.id,
                    'certificate_number': cert_number,
                    'status': 'issued',
                    'grade': request.data.get('grade', ''),
                    'notes': request.data.get('notes', ''),
                }
                
                serializer = self.get_serializer(data=certificate_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'Enrollment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# Admin/Instructor: Update certificate
class CertificateUpdateView(generics.UpdateAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Certificate.objects.all()

    def update(self, request, *args, **kwargs):
        user = request.user
        
        if user.role not in ['admin', 'instructor']:
            return Response(
                {'error': 'Only admin or instructor can update certificates.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


# Admin/Instructor: List all certificates
class CertificateListView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Only admin/instructor can list all
        if user.role not in ['admin', 'instructor']:
            return Certificate.objects.none()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            return Certificate.objects.filter(status=status_filter)
        
        return Certificate.objects.all()


# Admin/Instructor: Issue certificate (change status to 'issued')
@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def issue_certificate(request, pk):
    user = request.user
    
    if user.role not in ['admin', 'instructor']:
        return Response(
            {'error': 'Only admin or instructor can issue certificates.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        certificate = Certificate.objects.get(id=pk)
        certificate.status = 'issued'
        certificate.save()
        
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Certificate.DoesNotExist:
        return Response(
            {'error': 'Certificate not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
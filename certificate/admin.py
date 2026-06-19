from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'certificate_number',
        'student',
        'course',
        'status',
        'grade',
        'issue_date',
    )
    search_fields = (
        'certificate_number',
        'student__username',
        'course__name',
    )
    list_filter = ('status', 'issue_date', 'course')
    readonly_fields = ('certificate_number', 'issue_date')
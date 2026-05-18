from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'user', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    
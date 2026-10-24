from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = [
            'id',
            'candidate',
            'job',
            'resume',
            'ai_score',
            'status',
            'applied_at'
        ]
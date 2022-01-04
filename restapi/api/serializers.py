from rest_framework import serializers
from .models import BloodTest


class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodTest
        fields = ['id', 'client_ip', 'submit', 'client_file', 'parsing_completed', 'parsing_result']

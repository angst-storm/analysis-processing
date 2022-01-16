from rest_framework import serializers
from .models import BloodTest


class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodTest
        fields = ['id', 'parsing_completed', 'table_found', 'table_formatted', 'laboratory', 'parsing_result']

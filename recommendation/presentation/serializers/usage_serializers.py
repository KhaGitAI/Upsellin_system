from rest_framework import serializers
from recommendation.domain.models import ActivatedPackage, UsageLog

class ActivatedPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivatedPackage
        exclude = ['user']  # نحدد المستخدم من view

class UsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageLog
        fields = '__all__'

class UsageLogCreateSerializer(serializers.Serializer):
    internet_used = serializers.FloatField()
    call_used = serializers.IntegerField()
    sms_used = serializers.IntegerField()
    month = serializers.DateField(required=False)

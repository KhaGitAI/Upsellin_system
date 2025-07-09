from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from recommendation.domain.models import User as ProfileUser

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_staff:
            raise serializers.ValidationError("Only admin users can log in.")
        return data

class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

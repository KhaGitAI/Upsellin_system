from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from recommendation.domain.models import User as ProfileUser

class AdminRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return Response({"message": "Admin registered successfully"}, status=201)
    
class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_staff:
            raise serializers.ValidationError("Only admin users can log in.")

        data['refresh'] = str(self.get_token(self.user))
        data['access'] = str(self.get_token(self.user).access_token)
        data['username'] = self.user.username
        return data


class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer

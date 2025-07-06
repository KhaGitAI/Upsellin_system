from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from recommendation.domain.models import User 
from recommendation.presentation.serializers.auth_serializers import RegisterSerializer
from django.contrib.auth.hashers import check_password



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            auth_user = AuthUser.objects.create(
                username=serializer.validated_data['username'],
                password=make_password(serializer.validated_data['password'])
            )

            User.objects.create(
                auth_user=auth_user,
                age=serializer.validated_data['age'],
                phone_number= serializer.validated_data['phone_number'],
                gender=serializer.validated_data['gender'],
                line_type=serializer.validated_data['line_type'],
                location=serializer.validated_data['location'],
                signup_date=serializer.validated_data['signup_date'],
            )

            refresh = RefreshToken.for_user(auth_user)
            return Response({
                'message': 'User registered successfully.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({"error": "Phone number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = User.objects.get(phone_number=phone_number)
            auth_user = profile.auth_user

            if check_password(password, auth_user.password):
                refresh = RefreshToken.for_user(auth_user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
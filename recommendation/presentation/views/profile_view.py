from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.domain.models import User 
from recommendation.presentation.serializers.profile_serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_user = request.user
        try:
            profile = User.objects.get(auth_user=auth_user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Profile not found."}, status=404)
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully", "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

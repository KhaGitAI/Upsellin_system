from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.domain.models import User
from recommendation.presentation.serializers.profile_serializers import UserProfileSerializer
from django.db.models import Q
from django.db.models import Count

class UserListView(APIView):
    def get(self, request):
        gender = request.query_params.get("gender")
        line_type = request.query_params.get("line_type")
        location = request.query_params.get("location")
        age_range = request.query_params.get("age_range")

        filters = Q()

        if gender:
            filters &= Q(gender__iexact=gender)
        if line_type:
            filters &= Q(line_type__iexact=line_type)
        if location:
            filters &= Q(location__icontains=location)
        if age_range:
            filters &= Q(age_range=age_range)

        users = User.objects.filter(filters)
        serializer = UserProfileSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDistributionByAgeRange(APIView):
    def get(self, request):
        age_data = (
            User.objects.values('age_range')
            .annotate(user_count=Count('id'))
            .order_by('age_range')
        )
        return Response(age_data, status=status.HTTP_200_OK)
    
class UserDistributionByLocation(APIView):
    def get(self, request):
        location_data = (
            User.objects.values('location')
            .annotate(user_count=Count('id'))
            .order_by('-user_count')
        )
        return Response(location_data, status=status.HTTP_200_OK)

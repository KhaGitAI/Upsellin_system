from rest_framework import serializers
from recommendation.domain.models import User as ProfileUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['phone_number', 'age', 'gender', 'line_type', 'location', 'signup_date']

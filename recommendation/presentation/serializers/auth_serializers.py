from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from recommendation.domain.models import User as ProfileUser

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    age = serializers.IntegerField()
    gender = serializers.CharField()
    line_type = serializers.CharField()
    location = serializers.CharField()
    signup_date = serializers.DateField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AuthUser
        fields = ['username', 'password', 'phone_number', 'age', 'gender', 'line_type', 'location', 'signup_date']

    def create(self, validated_data):
        profile_data = {
            'phone_number': validated_data.pop('phone_number'),
            'age': validated_data.pop('age'),
            'gender': validated_data.pop('gender'),
            'line_type': validated_data.pop('line_type'),
            'location': validated_data.pop('location'),
            'signup_date': validated_data.pop('signup_date'),
        }

        user = AuthUser.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )

        ProfileUser.objects.create(
            auth_user=user,
            **profile_data
        )

        return user

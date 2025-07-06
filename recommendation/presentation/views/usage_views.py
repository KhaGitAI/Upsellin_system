from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Case, When, F, FloatField

from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from recommendation.domain.models import User,ActivatedPackage,UsageLog
from recommendation.presentation.serializers.usage_serializers import (
    ActivatedPackageSerializer,
    UsageLogSerializer,
    UsageLogCreateSerializer
)
from datetime import date
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser  
from django.db.models import Count, Avg, Sum, Max
from recommendation.application.usage_analysis import calculate_usage_percentages


class ActivePackageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            serializer = ActivatedPackageSerializer(data=request.data)
            if serializer.is_valid():
                ActivatedPackage.objects.create(
                    user=profile, 
                    **serializer.validated_data
                )
                return Response({"message": "Package activated successfully"}, status=201)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)


class UsedPackageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            latest_usage = UsageLog.objects.filter(user=profile, usage_type='PACKAGE').order_by('-month').first()

            if not latest_usage:
                return Response({"message": "No package usage data found."}, status=404)

            package = latest_usage.package  

            if not package:
                return Response({"message": "No package associated with usage."}, status=404)

            return Response({
                "package_name": package.package_name,
                "internet_limit": package.internet_limit,
                "call_limit": package.call_limit,
                "sms_limit": package.sms_limit,
                "price": package.price,
                "activation_date": package.activation_date,
                "end_date": package.end_date
            })

        except ActivatedPackage.DoesNotExist:
            return Response({"message": "Package not found."}, status=404)

        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=404)


class AddUsageLogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UsageLogCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                profile = User.objects.get(auth_user=request.user)
                usage_type = serializer.validated_data.get("usage_type", "PACKAGE")
                package = None

                if usage_type == "PACKAGE":
                    package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()
                    if not package:
                        return Response({"error": "No active package found."}, status=404)

                usage = UsageLog.objects.create(
                    user=profile,
                    month=serializer.validated_data.get("month", date.today()),
                    internet_used=serializer.validated_data["internet_used"],
                    call_used=serializer.validated_data["call_used"],
                    sms_used=serializer.validated_data["sms_used"],
                    usage_type=usage_type,
                    package=package
                )

                return Response({
                    "message": "Usage logged successfully",
                    "data": {
           
                        "month": usage.month,
                        "internet_used": usage.internet_used,
                        "call_used": usage.call_used,
                        "sms_used": usage.sms_used,
                        "usage_type": usage.usage_type,
                        "package_id": usage.package.id if usage.package else None
                    }
                }, status=201)

            except User.DoesNotExist:
                return Response({"error": "User profile not found."}, status=404)

        return Response(serializer.errors, status=400)


class ActivatedPackagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            packages = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date')
            serializer = ActivatedPackageSerializer(packages, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=404)


class UsageLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            usage_logs = UsageLog.objects.filter(user=profile).order_by('-month')
            serializer = UsageLogSerializer(usage_logs, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=404)


class UsagePercentageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)
            active_package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()
            usage = UsageLog.objects.filter(user=profile, package=active_package, usage_type='PACKAGE').order_by('-month').first()

            if not active_package or not usage:
                return Response({"message": "No active usage data found."}, status=404)
            usage_percentages = calculate_usage_percentages(usage, active_package)
            return Response(usage_percentages)
        except User.DoesNotExist:
            return Response({"error": "User profile not found."}, status=404)


class MonthlyUsageStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)

            usage_summary = (
                UsageLog.objects
                .filter(user=profile)
                .annotate(month_group=TruncMonth('month'))
                .values('month_group')
                .annotate(
                    flat_internet=Sum(
                        Case(When(usage_type='FLAT', then=F('internet_used')), output_field=FloatField())
                    ),
                    flat_call=Sum(
                        Case(When(usage_type='FLAT', then=F('call_used')), output_field=FloatField())
                    ),
                    flat_sms=Sum(
                        Case(When(usage_type='FLAT', then=F('sms_used')), output_field=FloatField())
                    ),
                    package_internet=Sum(
                        Case(When(usage_type='PACKAGE', then=F('internet_used')), output_field=FloatField())
                    ),
                    package_call=Sum(
                        Case(When(usage_type='PACKAGE', then=F('call_used')), output_field=FloatField())
                    ),
                    package_sms=Sum(
                        Case(When(usage_type='PACKAGE', then=F('sms_used')), output_field=FloatField())
                    ),
                )
                .order_by('-month_group')
            )

            results = []
            for item in usage_summary:
                results.append({
                    "month": item["month_group"].strftime("%Y-%m"),
                    "flat_usage": {
                        "internet_used": item["flat_internet"] or 0,
                        "call_used": item["flat_call"] or 0,
                        "sms_used": item["flat_sms"] or 0,
                    },
                    "package_usage": {
                        "internet_used": item["package_internet"] or 0,
                        "call_used": item["package_call"] or 0,
                        "sms_used": item["package_sms"] or 0,
                    },
                    "total_usage": {
                        "internet_used": (item["flat_internet"] or 0) + (item["package_internet"] or 0),
                        "call_used": (item["flat_call"] or 0) + (item["package_call"] or 0),
                        "sms_used": (item["flat_sms"] or 0) + (item["package_sms"] or 0),
                    }
                })

            return Response(results)

        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)
        
        
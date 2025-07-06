from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.domain.models import User, UsageLog,UsageLog,Prediction,ActivatedPackage,SuggestedPackage
from recommendation.presentation.serializers.profile_serializers import UserProfileSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404


class UserDetailView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile_data = UserProfileSerializer(user).data

        usage_logs = (
            UsageLog.objects
            .filter(user=user)
            .order_by('month')
            .values('month')
            .annotate(
                total_internet=Sum('internet_used'),
                total_calls=Sum('call_used'),
                total_sms=Sum('sms_used')
            )
        )

        profile_data["monthly_usage"] = list(usage_logs)

        return Response(profile_data, status=status.HTTP_200_OK)
    
    
class UserUsageDetailsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        usage_logs = (
            UsageLog.objects
            .filter(user=user)
            .order_by('-month')
            .values(
                'month',
                'internet_used',
                'call_used',
                'sms_used',
                'usage_type',
                'package__package_name'
            )
        )

        return Response(list(usage_logs), status=status.HTTP_200_OK)

class UserPredictionVsActualView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        predictions = Prediction.objects.filter(user=user).order_by('predicted_month')
        prediction_map = {
            pred.predicted_month: pred for pred in predictions
        }

        suggested_packages = SuggestedPackage.objects.filter(user=user)
        suggested_map = {
            p.Final_date: p for p in suggested_packages
        }

        activated_packages = ActivatedPackage.objects.filter(user=user)
        activated_map = {
            a.activation_date: a for a in activated_packages
        }

        usage_logs = UsageLog.objects.filter(user=user).order_by('month')

        result = []

        for usage in usage_logs:
            month = usage.month
            pred = prediction_map.get(month)
            suggested = suggested_map.get(month)
            activated = activated_map.get(month)

            result.append({
                "month": month,

                # Actual vs Predicted
                "actual_internet": usage.internet_used,
                "predicted_internet": pred.predicted_internet if pred else None,
                "diff_internet": usage.internet_used - pred.predicted_internet if pred else None,

                "actual_calls": usage.call_used,
                "predicted_calls": pred.predicted_calls if pred else None,
                "diff_calls": usage.call_used - pred.predicted_calls if pred else None,

                "actual_sms": usage.sms_used,
                "predicted_sms": pred.predicted_price if pred else None,  # أو sms إن توفر
                "diff_sms": usage.sms_used - pred.predicted_price if pred else None,

                # Suggested & Activated packages
                "suggested_package": {
                    "internet": suggested.Final_internet,
                    "calls": suggested.Final_calls,
                    "sms": suggested.Final_sms,
                    "price": suggested.Final_price,
                } if suggested else None,

                "activated": bool(activated),
                "activation_date": activated.activation_date if activated else None,
                "package_name": activated.package_name if activated else None,
            })

        return Response(result, status=status.HTTP_200_OK)

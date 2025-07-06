from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
from recommendation.domain.models import User ,ActivatedPackage,UsageLog,SuggestedPackage,FeedbackLog

from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser  
from django.db.models import Count, Avg, Sum, Max
from recommendation.application.usage_analysis import calculate_usage_percentages
from recommendation.application.performance_report import evaluate_user_performance

class UserPerformanceReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = User.objects.get(auth_user=request.user)

            package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()
            if not package:
                return Response({"error": "No active package found."}, status=404)

            usage = UsageLog.objects.filter(user=profile, package=package).order_by('-month').first()
            if not usage:
                return Response({"error": "No usage found for the package."}, status=404)

            report = evaluate_user_performance(request.user, usage, package)
            return Response(report)

        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class SystemReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        avg_age = User.objects.aggregate(average_age=Avg('age'))['average_age']
        gender_dist = User.objects.values('gender').annotate(count=Count('id'))

        total_packages = ActivatedPackage.objects.count()
        active_packages = ActivatedPackage.objects.filter(end_date__gte=date.today()).count()
        expired_packages = ActivatedPackage.objects.filter(end_date__lt=date.today()).count()

        total_usage = UsageLog.objects.aggregate(
            total_internet=Sum('internet_used'),
            total_calls=Sum('call_used'),
            total_sms=Sum('sms_used')
        )

        usage_per_user = UsageLog.objects.values('user').annotate(
            total_used=Sum('internet_used') + Sum('call_used') + Sum('sms_used')
        ).order_by('-total_used')

        top_user_id = usage_per_user[0]['user'] if usage_per_user else None
        top_user_name = User.objects.get(id=top_user_id).auth_user.username if top_user_id else None

        report = {
            "users": {
                "total": total_users,
                "average_age": round(avg_age, 1) if avg_age else 0,
                "gender_distribution": {g['gender']: g['count'] for g in gender_dist}
            },
            "packages": {
                "total_activated": total_packages,
                "currently_active": active_packages,
                "expired": expired_packages
            },
            "usage": {
                "total_internet_used": total_usage['total_internet'],
                "total_call_minutes_used": total_usage['total_calls'],
                "total_sms_used": total_usage['total_sms'],
                "top_user": top_user_name
            }
        }

        return Response(report)

class AIPerformanceReportView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        total_suggestions = SuggestedPackage.objects.count()
        activated_suggestions = ActivatedPackage.objects.filter(suggested_package__isnull=False).count()
        feedback_count = FeedbackLog.objects.count()

        suggestions = SuggestedPackage.objects.all()
        total_accuracy = 0
        total_satisfaction = 0
        count = 0

        for s in suggestions:
            usage = UsageLog.objects.filter(user=s.user, package_id=s.id).order_by('-month').first()
            if usage:
                internet_accuracy = min(usage.internet_used / s.Final_internet, 1.0)
                call_accuracy = min(usage.call_used / s.Final_calls, 1.0)
                sms_accuracy = min(usage.sms_used / s.Final_sms, 1.0)

                average_accuracy = round((internet_accuracy + call_accuracy + sms_accuracy) / 3, 2)
                total_accuracy += average_accuracy

                if average_accuracy >= 0.7:
                    total_satisfaction += 1

                count += 1

        average_accuracy_percent = round((total_accuracy / count) * 100, 2) if count else 0
        satisfaction_percent = round((total_satisfaction / count) * 100, 2) if count else 0

        return Response({
            "total_suggestions": total_suggestions,
            "suggestions_activated": activated_suggestions,
            "prediction_accuracy_percent": average_accuracy_percent,
            "user_feedback_count": feedback_count,
            "user_satisfaction_percent": satisfaction_percent
        })

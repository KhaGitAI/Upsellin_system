from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum, Q

from recommendation.domain.models import User, UsageLog, SuggestedPackage, FeedbackLog

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Q
from recommendation.domain.models import User, UsageLog, SuggestedPackage, FeedbackLog


class HomeDashboardView(APIView):
    def get(self, request):
        try:
            total_users = User.objects.count()
            male_count = User.objects.filter(gender__iexact="male").count()
            female_count = User.objects.filter(gender__iexact="female").count()

            male_percent = (male_count / total_users * 100) if total_users else 0
            female_percent = (female_count / total_users * 100) if total_users else 0

            # استهلاك حسب الجنس
            usage_by_gender = (
                User.objects.values('gender')
                .annotate(
                    internet=Sum('usagelog__internet_used'),
                    calls=Sum('usagelog__call_used'),
                    sms=Sum('usagelog__sms_used')
                )
            )

            # استهلاك حسب المحافظة
            usage_by_location = (
                User.objects.values('location')
                .annotate(
                    total_usage=Sum('usagelog__internet_used') +
                                Sum('usagelog__call_used') +
                                Sum('usagelog__sms_used')
                )
                .order_by('-total_usage')
            )

            top_locations = usage_by_location[:5]

            # إحصائيات الاقتراحات
            suggested_count = SuggestedPackage.objects.count()
            accepted_count = FeedbackLog.objects.filter(accepted=True).count()

            return Response({
                "total_users": total_users,
                "male_users": {
                    "count": male_count,
                    "percentage": round(male_percent, 2)
                },
                "female_users": {
                    "count": female_count,
                    "percentage": round(female_percent, 2)
                },
                "consumption_by_gender": list(usage_by_gender),
                "consumption_by_location": list(usage_by_location),
                "top_locations": list(top_locations),
                "upselling": {
                    "suggested_count": suggested_count,
                    "accepted_count": accepted_count
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

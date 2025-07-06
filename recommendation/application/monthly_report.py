from django.db.models.functions import TruncMonth
from django.db.models import Sum

def generate_monthly_summary(queryset):
    summary = (
        queryset
        .annotate(month_group=TruncMonth('month'))
        .values('month_group')
        .annotate(
            internet_used=Sum('internet_used'),
            call_used=Sum('call_used'),
            sms_used=Sum('sms_used'),
        )
        .order_by('-month_group')
    )

    return [
        {
            "month": item["month_group"].strftime("%Y-%m"),
            "internet_used": item["internet_used"],
            "call_used": item["call_used"],
            "sms_used": item["sms_used"],
        }
        for item in summary
    ]

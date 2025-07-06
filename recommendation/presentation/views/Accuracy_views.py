from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.domain.models import Prediction
from recommendation.domain.models import UsageLog
from recommendation.domain.models import PredictionAccuracyLog
# from recommendation.serializers import PredictionAccuracySerializer
from datetime import datetime

class GeneratePredictionAccuracyView(APIView):
    def post(self, request):
        month_str = request.data.get("month")  # بصيغة YYYY-MM-DD
        if not month_str:
            return Response({"error": "month is required"}, status=400)
        
        try:
            month = datetime.strptime(month_str, "%Y-%m-%d").date()
        except:
            return Response({"error": "Invalid date format"}, status=400)

        created = 0
        predictions = Prediction.objects.filter(predicted_month=month)
        for prediction in predictions:
            try:
                usage = UsageLog.objects.get(user=prediction.user, month=month)
                PredictionAccuracy.objects.create(
                    user=prediction.user,
                    prediction=prediction,
                    usage_log=usage,
                    month=month,
                    predicted_internet=prediction.predicted_internet,
                    actual_internet=usage.internet_used,
                    diff_internet=abs(prediction.predicted_internet - usage.internet_used),
                    predicted_calls=prediction.predicted_calls,
                    actual_calls=usage.call_used,
                    diff_calls=abs(prediction.predicted_calls - usage.call_used)
                )
                created += 1
            except UsageLog.DoesNotExist:
                continue

        return Response({"message": f"Created {created} accuracy records."}, status=201)

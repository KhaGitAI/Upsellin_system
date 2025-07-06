from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recommendation.domain.models import AIModelMetrics
from rest_framework.permissions import AllowAny
from recommendation.core.premmission import IsAdminUser 
class AIPerformanceReportView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            latest = AIModelMetrics.objects.latest('created_at')

            data = {
                "accuracy": latest.accuracy,
                "precision": latest.precision,
                "recall": latest.recall,
                "f1_score": latest.f1_score,
                "roc_auc": latest.roc_auc,
                "pr_auc": latest.pr_auc,
                "confusion_matrix": latest.confusion_matrix_json,
                "additional_info": latest.additional_info
            }

            return Response(data, status=status.HTTP_200_OK)

        except AIModelMetrics.DoesNotExist:
            return Response({"error": "No metrics available."}, status=status.HTTP_404_NOT_FOUND)

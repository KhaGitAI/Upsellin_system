from django.contrib import admin

# Register your models here.
from recommendation.domain.models import (
    User,
    Prediction,
    UsageLog,
    SuggestedPackage,
    ActivatedPackage,
    CustomPackage,
    Cluster,
    FeedbackLog,
    AIModelMetrics,
    PredictionAccuracyLog,
)

admin.site.register(User)
admin.site.register(Prediction)
admin.site.register(UsageLog)
admin.site.register(SuggestedPackage)
admin.site.register(ActivatedPackage)
admin.site.register(CustomPackage)
admin.site.register(Cluster)
admin.site.register(FeedbackLog)
admin.site.register(AIModelMetrics)
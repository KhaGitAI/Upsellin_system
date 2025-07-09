from django.urls import path
from recommendation.presentation.views.auth_views import RegisterView, LoginView
from recommendation.presentation.views.profile_view import UserProfileView, UpdateProfileView
from recommendation.presentation.views.stats_views import HomeDashboardView
from recommendation.presentation.views.AI_report_view import AIModelMetrics
from recommendation.presentation.views.admin_auth import AdminRegisterView,AdminLoginView

from recommendation.presentation.views.usage_views import (
    ActivePackageView, AddUsageLogView, ActivatedPackagesView,
    UsageLogListView, UsagePercentageView, MonthlyUsageStatsView
)
from recommendation.presentation.views.Accuracy_views import GeneratePredictionAccuracyView
# from recommendation.domain import PredictionsAccuracyLog
# from recommendation.presentation.views.report_view import AIPerformanceReportView

from recommendation.presentation.views.User_profile import (UserDetailView,UserUsageDetailsView,UserPredictionVsActualView)

from recommendation.presentation.views.report_view import (
    UserPerformanceReportView, SystemReportView, AIPerformanceReportView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from recommendation.presentation.views.Alluser_views import (
    UserListView,
    UserDistributionByAgeRange,
    UserDistributionByLocation
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='get_user_profile'),
    path('profile/update', UpdateProfileView.as_view(), name='update_user_profile'),
    path('package/active/', ActivePackageView.as_view(), name='active_package'),
    path('usage/add/', AddUsageLogView.as_view(), name='add_usage_log'),
    path('package/activated/', ActivatedPackagesView.as_view(), name='get_activated_packages'),
    path('usage/', UsageLogListView.as_view(), name='get_usage_logs'),
    path('usage/percentage/', UsagePercentageView.as_view(), name='usage_percentage'),
    path('usage/monthly/', MonthlyUsageStatsView.as_view(), name='monthly_usage'),
    path('report/performance/', UserPerformanceReportView.as_view(), name='performance_report'),
    path('report/system/', SystemReportView.as_view(), name='system_report'),
    # path('report/ai/', AIPerformanceReportView.as_view(), name='ai_report'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/home/', HomeDashboardView.as_view(),name="dashboard_home"),
    path('users/list/', UserListView.as_view(), name="user_list"),
    path('users/distribution/age-range/', UserDistributionByAgeRange.as_view(), name="user_distribution_age"),
    path('users/distribution/location/', UserDistributionByLocation.as_view(), name="user_distribution_location"),
    path('users/<int:user_id>/profile/', UserDetailView.as_view(), name="user_profile"),
    path('users/<int:user_id>/usage-details/', UserUsageDetailsView.as_view(), name="user_usage_details"),
    path('users/<int:user_id>/prediction-vs-actual/', UserPredictionVsActualView.as_view(), name="user_prediction_vs_actual"),
    path('report/ai/', AIPerformanceReportView.as_view(), name="ai_report"), 
    path("accuracy/", GeneratePredictionAccuracyView.as_view()),
    path("admin/register/", AdminRegisterView.as_view()),
    path("admin/login/", AdminLoginView.as_view()),

]
    




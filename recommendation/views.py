# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User as AuthUser
# from django.contrib.auth.hashers import make_password
# from .domain.models import User ,ActivatedPackage,UsageLog,SuggestedPackage
# from .serializers import RegisterSerializer
# from .domain.models import User  ,FeedbackLog
# from django.contrib.auth.hashers import check_password
# from rest_framework.permissions import IsAuthenticated
# from .serializers import UserProfileSerializer,ActivatedPackageSerializer,UsageLogCreateSerializer,UsageLogSerializer
# from datetime import date
# from django.db.models.functions import TruncMonth
# from django.db.models import Sum
# from rest_framework.permissions import IsAdminUser  
# from django.db.models import Count, Avg, Sum, Max
# from recommendation.application.usage_analysis import calculate_usage_percentages

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             auth_user = AuthUser.objects.create(
#                 username=serializer.validated_data['username'],
#                 password=make_password(serializer.validated_data['password'])
#             )

#             User.objects.create(
#                 auth_user=auth_user,
#                 age=serializer.validated_data['age'],
#                 phone_number= serializer.validated_data['phone_number'],
#                 gender=serializer.validated_data['gender'],
#                 line_type=serializer.validated_data['line_type'],
#                 location=serializer.validated_data['location'],
#                 signup_date=serializer.validated_data['signup_date'],
#             )

#             refresh = RefreshToken.for_user(auth_user)
#             return Response({
#                 'message': 'User registered successfully.',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class LoginView(APIView):
#     def post(self, request):
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')

#         if not phone_number or not password:
#             return Response({"error": "Phone number and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             profile = User.objects.get(phone_number=phone_number)
#             auth_user = profile.auth_user

#             if check_password(password, auth_user.password):
#                 refresh = RefreshToken.for_user(auth_user)
#                 return Response({
#                     'message': 'Login successful',
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         auth_user = request.user
#         try:
#             profile = User.objects.get(auth_user=auth_user)
#             serializer = UserProfileSerializer(profile)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response({"error": "Profile not found."}, status=404)
# class UpdateProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             serializer = UserProfileSerializer(profile, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Profile updated successfully", "data": serializer.data})
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)


# class ActivePackageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             serializer = ActivatedPackageSerializer(data=request.data)
#             if serializer.is_valid():
#                 ActivatedPackage.objects.create(
#                     user=profile, 
#                     **serializer.validated_data
# )

#                 return Response({"message": "Package activated successfully"}, status=201)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User profile not found"}, status=404)
        
        
# class UsedPackageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             latest_usage = UsageLog.objects.filter(user=profile).order_by('-month').first()

#             if not latest_usage:
#                 return Response({"message": "No usage data found."}, status=404)

#             if latest_usage.package_id is None:
#                 return Response({"message": "No package used in latest usage record."}, status=404)

#             try:
#                 package = ActivatedPackage.objects.get(id=latest_usage.package_id)
#                 return Response({
#                     "package_name": package.package_name,
#                     "internet_limit": package.internet_limit,
#                     "call_limit": package.call_limit,
#                     "sms_limit": package.sms_limit,
#                     "price": package.price,
#                     "activation_date": package.activation_date,
#                     "end_date": package.end_date
#                 })
#             except ActivatedPackage.DoesNotExist:
#                 return Response({"message": "Package not found."}, status=404)

#         except User.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=404)
        
        
# class AddUsageLogView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = UsageLogCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 profile = User.objects.get(auth_user=request.user)
#                 active_package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()

#                 if not active_package:
#                     return Response({"error": "No active package found."}, status=404)

#                 usage = UsageLog.objects.create(
#                     user=profile,
#                     month=serializer.validated_data.get("month", date.today()),
#                     internet_used=serializer.validated_data["internet_used"],
#                     call_used=serializer.validated_data["call_used"],
#                     sms_used=serializer.validated_data["sms_used"],
#                     package_id=active_package.id
#                 )

#                 return Response({
#                     "message": "Usage logged successfully",
#                     "data": {
#                         "month": usage.month,
#                         "internet_used": usage.internet_used,
#                         "call_used": usage.call_used,
#                         "sms_used": usage.sms_used,
#                         "package_id": usage.package_id
#                     }
#                 }, status=201)

#             except User.DoesNotExist:
#                 return Response({"error": "User profile not found."}, status=404)
        
#         return Response(serializer.errors, status=400)
    
    
# class ActivatedPackagesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             packages = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date')
#             serializer = ActivatedPackageSerializer(packages, many=True)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=404)
        
        
# class UsageLogListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             usage_logs = UsageLog.objects.filter(user=profile).order_by('-month')
#             serializer = UsageLogSerializer(usage_logs, many=True)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=404)
        
        
# #show Percentage from the Bundle
# class UsagePercentageView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             active_package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()
#             usage = UsageLog.objects.filter(user=profile, package_id=active_package.id).order_by('-month').first()

#             if not active_package or not usage:
#                 return Response({"message": "No active usage data found."}, status=404)
#             usage_percentages = calculate_usage_percentages(usage, active_package)
#             return Response(usage_percentages)
#         except User.DoesNotExist:
#             return Response({"error": "User profile not found."}, status=404)


# class MonthlyUsageStatsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
            
#             usage_summary = (
#                 UsageLog.objects
#                 .filter(user=profile)
#                 .annotate(month_group=TruncMonth('month'))
#                 .values('month_group')

#                 .annotate(
#                     internet_used=Sum('internet_used'),
#                     call_used=Sum('call_used'),
#                     sms_used=Sum('sms_used'),
#                 )
#                 .order_by('-month')
#             )

#             results = [
#                 {
#                     "month": item["month_group"].strftime("%Y-%m"),
#                     "internet_used": item["internet_used"],
#                     "call_used": item["call_used"],
#                     "sms_used": item["sms_used"],
#                 }
#                 for item in usage_summary
#             ]

#             return Response(results)

#         except User.DoesNotExist:
#             return Response({"error": "User profile not found"}, status=404)
        
        
# class UserPerformanceReportView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             profile = User.objects.get(auth_user=request.user)
#             package = ActivatedPackage.objects.filter(user=profile).order_by('-activation_date').first()
#             usage = UsageLog.objects.filter(user=profile, package_id=package.id).order_by('-month').first()

#             def calc_percent(used, limit):
#                 return round((used / limit) * 100, 2) if limit > 0 else 0

#             report = {
#                 "user": request.user.username,
#                 "month": usage.month.strftime("%Y-%m"),
#                 "package_name": package.package_name,
#                 "internet_used": usage.internet_used,
#                 "internet_limit": package.internet_limit,
#                 "internet_usage_percent": calc_percent(usage.internet_used, package.internet_limit),
#                 "call_used": usage.call_used,
#                 "call_limit": package.call_limit,
#                 "call_usage_percent": calc_percent(usage.call_used, package.call_limit),
#                 "sms_used": usage.sms_used,
#                 "sms_limit": package.sms_limit,
#                 "sms_usage_percent": calc_percent(usage.sms_used, package.sms_limit),
#             }

#             total_usage = (
#                 calc_percent(usage.internet_used, package.internet_limit) +
#                 calc_percent(usage.call_used, package.call_limit) +
#                 calc_percent(usage.sms_used, package.sms_limit)
#             ) / 3

#             if total_usage < 30:
#                 report["status"] = "Low Usage"
#             elif total_usage < 80:
#                 report["status"] = "Moderate Usage"
#             else:
#                 report["status"] = "Good Usage"

#             return Response(report)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

# class SystemReportView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         total_users = User.objects.count()
#         avg_age = User.objects.aggregate(average_age=Avg('age'))['average_age']
#         gender_dist = User.objects.values('gender').annotate(count=Count('id'))

#         total_packages = ActivatedPackage.objects.count()
#         active_packages = ActivatedPackage.objects.filter(end_date__gte=date.today()).count()
#         expired_packages = ActivatedPackage.objects.filter(end_date__lt=date.today()).count()

#         total_usage = UsageLog.objects.aggregate(
#             total_internet=Sum('internet_used'),
#             total_calls=Sum('call_used'),
#             total_sms=Sum('sms_used')
#         )

#         usage_per_user = UsageLog.objects.values('user').annotate(
#             total_used=Sum('internet_used') + Sum('call_used') + Sum('sms_used')
#         ).order_by('-total_used')

#         top_user_id = usage_per_user[0]['user'] if usage_per_user else None
#         top_user_name = User.objects.get(id=top_user_id).auth_user.username if top_user_id else None

#         report = {
#             "users": {
#                 "total": total_users,
#                 "average_age": round(avg_age, 1) if avg_age else 0,
#                 "gender_distribution": {g['gender']: g['count'] for g in gender_dist}
#             },
#             "packages": {
#                 "total_activated": total_packages,
#                 "currently_active": active_packages,
#                 "expired": expired_packages
#             },
#             "usage": {
#                 "total_internet_used": total_usage['total_internet'],
#                 "total_call_minutes_used": total_usage['total_calls'],
#                 "total_sms_used": total_usage['total_sms'],
#                 "top_user": top_user_name
#             }
#         }

#         return Response(report)

# class AIPerformanceReportView(APIView):
#     permission_classes = [IsAdminUser]  

#     def get(self, request):
#         total_suggestions = SuggestedPackage.objects.count()
#         activated_suggestions = ActivatedPackage.objects.filter(suggested_package__isnull=False).count()
#         feedback_count = FeedbackLog.objects.count()

#         # تحليل الاستخدام الفعلي مقابل التوصية
#         suggestions = SuggestedPackage.objects.all()
#         total_accuracy = 0
#         total_satisfaction = 0
#         count = 0

#         for s in suggestions:
#             usage = UsageLog.objects.filter(user=s.user, package_id=s.id).order_by('-month').first()
#             if usage:
#                 # احسب نسب الاستخدام لكل نوع
#                 internet_accuracy = min(usage.internet_used / s.Final_internet, 1.0)
#                 call_accuracy = min(usage.call_used / s.Final_calls, 1.0)
#                 sms_accuracy = min(usage.sms_used / s.Final_sms, 1.0)

#                 average_accuracy = round((internet_accuracy + call_accuracy + sms_accuracy) / 3, 2)
#                 total_accuracy += average_accuracy

#                 if average_accuracy >= 0.7:
#                     total_satisfaction += 1

#                 count += 1

#         average_accuracy_percent = round((total_accuracy / count) * 100, 2) if count else 0
#         satisfaction_percent = round((total_satisfaction / count) * 100, 2) if count else 0

#         return Response({
#             "total_suggestions": total_suggestions,
#             "suggestions_activated": activated_suggestions,
#             "prediction_accuracy_percent": average_accuracy_percent,
#             "user_feedback_count": feedback_count,
#             "user_satisfaction_percent": satisfaction_percent
#         })
       
from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.
class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    line_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    signup_date = models.DateField()
    age_range = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"User {self.auth_user.username}"
    

class SuggestedPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Final_internet = models.FloatField()
    Final_calls = models.IntegerField()
    Final_sms = models.IntegerField()
    Final_price = models.FloatField()
    generated_from_prediction = models.ForeignKey("Prediction", on_delete=models.CASCADE)
    Final_date = models.DateField()
 

    
    
    
class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_internet = models.FloatField()
    predicted_calls = models.IntegerField()
    predicted_price = models.FloatField()
    predicted_month = models.DateField()
    class Meta:
        abstract = False
        
     
class ActivatedPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_package = models.ForeignKey(SuggestedPackage, null=True, on_delete=models.SET_NULL,blank=True)
    package_name = models.CharField(max_length=100)
    internet_limit = models.FloatField()
    call_limit = models.IntegerField()
    sms_limit = models.IntegerField()
    price = models.FloatField()
    activation_date = models.DateField()
    end_date = models.DateField()
        
class UsageLog(models.Model):
    USAGE_TYPE_CHOICES = [
        ('PACKAGE', 'From Package'),
        ('FLAT', 'Flat Usage'),  
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    internet_used = models.FloatField()
    call_used = models.IntegerField()
    sms_used = models.IntegerField()
    usage_type = models.CharField(max_length=10, choices=USAGE_TYPE_CHOICES, default='PACKAGE')
    package = models.ForeignKey(ActivatedPackage, null=True, blank=True, on_delete=models.SET_NULL, related_name="usage_logs")

    def __str__(self):
        return f"{self.user} - {self.usage_type} - {self.month}"
    
    



class CustomPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_package = models.ForeignKey(SuggestedPackage, null=True, on_delete=models.SET_NULL,blank=True)
    internet = models.FloatField()
    calls = models.IntegerField()
    sms = models.FloatField()
    price = models.FloatField()
    customization_date = models.DateField()
    
class Cluster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cluster_id = models.IntegerField()
    label_per_user = models.CharField(max_length=100, null=True)
    
class FeedbackLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_package = models.ForeignKey(SuggestedPackage, on_delete=models.CASCADE)
    actual_usage_internet = models.FloatField()
    actual_usage_calls = models.IntegerField()
    actual_usage_sms = models.IntegerField()
    feedback_date = models.DateField()
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    accepted = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Feedback from {self.user} on {self.package}"
    
    
class AIModelMetrics(models.Model):
    evaluation_date = models.DateField(auto_now_add=True)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    roc_auc = models.FloatField(null=True, blank=True)
    pr_auc = models.FloatField(null=True, blank=True)
    confusion_matrix_json = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Model {self.model_version} - {self.evaluation_date}"
    
    
    
class PredictionAccuracyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    usage_log = models.ForeignKey(UsageLog, on_delete=models.CASCADE)
    
    month = models.DateField()
    predicted_internet = models.FloatField()
    actual_internet = models.FloatField()
    diff_internet = models.FloatField()
    
    predicted_calls = models.IntegerField()
    actual_calls = models.IntegerField()
    diff_calls = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.month}"
  
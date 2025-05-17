from django.db import models

# Create your models here.
class User(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=10 )
    line_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    signup_date = models.DateField()

    def __str__(self):
        return f"User {self.id}"
    
class UsageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    internet_used = models.FloatField()
    call_used = models.IntegerField()
    sms_used = models.IntegerField()
    package_id = models.IntegerField(null=True)
    
class ActivatedPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    internet_limit = models.FloatField()
    call_limit = models.IntegerField()
    sms_limit = models.IntegerField()
    price = models.FloatField()
    activation_date = models.DateField()
    end_date = models.DateField()
    
class XgboostPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_internet = models.FloatField()
    predicted_calls = models.IntegerField()
    predicted_price = models.FloatField()
    predicted_month = models.DateField()
    

class SuggestedPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Final_internet = models.FloatField()
    Final_calls = models.IntegerField()
    Final_sms = models.IntegerField()
    Final_price = models.FloatField()
    generated_from_prediction = models.ForeignKey(XgboostPrediction, on_delete=models.CASCADE)
    Final_date = models.DateField()
 
class CustomPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggested_package = models.ForeignKey(SuggestedPackage, on_delete=models.CASCADE)
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
    prediction = models.ForeignKey(XgboostPrediction, on_delete=models.CASCADE)

from django.db import models



class regtable(models.Model):
    name=models.CharField(max_length=150)
    phone_number=models.CharField(max_length=120)
    email=models.CharField(max_length=120)
    password=models.CharField(max_length=120)

class Prediction(models.Model):
    user = models.ForeignKey(regtable, on_delete=models.CASCADE)
    ph = models.FloatField()
    Hardness = models.FloatField()
    Solids = models.FloatField()
    Chloramines = models.FloatField()
    Sulfate = models.FloatField()
    Conductivity = models.FloatField()
    Organic_carbon = models.FloatField()
    Trihalomethanes = models.FloatField()
    Turbidity = models.FloatField()
    result = models.CharField(max_length=20)  # 'Potable' or 'Not Potable'
    created_at = models.DateTimeField(auto_now_add=True)

class Staff(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)

class Feedback(models.Model):
    user = models.ForeignKey(regtable, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

from django.db import models
from rest_framework import serializers

# Create your models here.
class AdminAccount(models.Model):
    SId = models.AutoField(primary_key=True)
    SFname=models.CharField(max_length=100, default="First Name")
    SLname=models.CharField(max_length=100, default="Last Name")
    SEmail=models.CharField(max_length=100, default="Email Name")
    SUsername=models.CharField(max_length=100, default="Username ")
    SPassword=models.TextField(max_length=3000, default="Password ")
    SContactNo=models.CharField(max_length=100, default="Contact no")
    SProfile= models.ImageField(upload_to='SuperAdmin/',default="dummy.jpg")
    def __str__(self):
        return self.SFname

class Seradmin(serializers.ModelSerializer):
    class Meta:
        model= AdminAccount
        fields=('SId','SFname','SLname','SUsername','SEmail','SContactNo','SProfile')
    
    

class Packages(models.Model):
    PackId=models.AutoField(primary_key=True)
    PackName=models.CharField(max_length=300, default="Package Name")
    PackDescription=models.TextField(max_length=3300, default="Package Description")
    PackStudent = models.IntegerField(default=0)
    PackTeacher = models.IntegerField(default=0)
    PackDurationStart=models.DateField()
    PackDurationEnd=models.DateField()
    PackPrice= models.FloatField(default=0.0)
    def __str__(self):
        return self.PackName

class Serpackage(serializers.ModelSerializer):
    class Meta:
        model= Packages
        fields=('PackId','PackName','PackDescription','PackStudent','PackTeacher','PackDurationStart','PackDurationEnd','PackPrice')
    






  


# Create your models here.
from django.db import models
from UniversityApp.models import UniversityAccount , UniversityBranch
from rest_framework import serializers

# Create your models here.
class Contact(models.Model): 

    Full_name=models.CharField(max_length=150,default="")
    Email=models.CharField(max_length=70,default="")
    subject=models.CharField(max_length=100,default="")
    Message=models.TextField(max_length=1000,default="dummy")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)


    def __str__(self):
        return self.Full_name

class SerContact(serializers.ModelSerializer):
    class Meta:
        model= Contact
        fields=('Message','Full_name','Email')
    
    
class User_Signup(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,default="")
    email = models.CharField(max_length=100,default="")
    password = models.TextField(default='')
    role=models.CharField(max_length=50,default="null")
    token=models.TextField(default=0)
    verify=models.CharField(max_length=100,default="unverified")  
   
   

    def __str__(self):
        return self.username
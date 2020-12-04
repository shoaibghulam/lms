from django.db import models
from SuperAdmin.models import AdminAccount , Packages
from datetime import datetime
from rest_framework import serializers
UNISTATUS=(
    ('Active','Active'),
    ('Disable','Disable'),
)
# Create your models here.
class UniversityAccount(models.Model):
    UniId= models.AutoField(primary_key=True)
    UniName=models.CharField(max_length=500, default="Uni Name")
    UniUsername=models.CharField(max_length=100, default="Uni Username")
    UniEmail=models.CharField(max_length=100, default="Uni Email")
    UniPassword=models.TextField(max_length=3000, default="Uni Password")
    UniAddress=models.CharField(max_length=100, default="Uni Address")
    UniStatus=models.CharField(max_length=80, choices=UNISTATUS , default="Disable")
    UniLogo = models.ImageField(upload_to="university/", default="logo.png")
    UniPackage=models.ForeignKey(Packages , on_delete=models.CASCADE)
    SuperId=models.ForeignKey(AdminAccount, on_delete=models.CASCADE)
    def __str__(self):
        return self.UniName
    
class SerUni(serializers.ModelSerializer):
    class Meta:
        model= UniversityAccount
        fields=('UniId','UniName','UniUsername','UniEmail','UniPassword','UniAddress','UniStatus','UniPackage','SuperId')



class UniversityBranch(models.Model):
    BranchId=models.AutoField(primary_key=True)
    BranchName=models.CharField(max_length=400 , default="Branch Name")
    BranchUsername=models.CharField(max_length=400 , default="Branch Username")
    BranchEmail=models.CharField(max_length=400 , default="Branch Email")
    BranchPassword=models.TextField(max_length=3000 , default="Branch Password")
    BranchAddress=models.CharField(max_length=400 , default="Branch Address")
    BranchCreatedDate=models.DateTimeField(blank=True)
    UniversityId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    def __str__(self):
        return self.BranchName

class Serbranch(serializers.ModelSerializer):
    class Meta:
        model= UniversityBranch
        fields=('BranchId','BranchName','BranchUsername','BranchEmail','BranchPassword','BranchAddress','BranchCreatedDate','UniversityId')

    
    




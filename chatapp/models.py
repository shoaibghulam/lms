from django.db import models
from faculty.models import Instructor
from student .models import Student_Profile
from datetime import datetime    
from rest_framework import serializers
from UniversityApp.models import UniversityAccount , UniversityBranch
# Create your models here.
class messages(models.Model):
    msgid = models.AutoField(primary_key=True)
    msgfrom = models.IntegerField()
    msgto = models.IntegerField()
    msg = models.TextField(max_length=3000)
    sender_name= models.CharField(max_length=100)
    is_read= models.IntegerField(default=0)
    created_at= models.CharField(max_length=100)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.sender_name

# messages seralizer
class sermessages(serializers.ModelSerializer):
    class Meta:
        model = messages
        fields = '__all__'
    

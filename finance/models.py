from django.db import models
from rest_framework import serializers
from datetime import datetime
from UniversityApp.models import UniversityAccount , UniversityBranch
from faculty.models import Instructor
from student.models import Student_Profile
# Create your models here.
class FianceUser(models.Model):
    Fid= models.AutoField(primary_key=True)
    FirstName=models.CharField(max_length=60, default="First Name")
    LastName=models.CharField(max_length=60, default="Last Name")
    Email= models.CharField(max_length=100, default="youremail@gmail.com")
    Password=models.TextField(max_length=1300)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Email



class TeacherSalary(models.Model):
    SalaryId= models.AutoField(primary_key=True)
    IssueDate=models.DateTimeField(auto_now_add=True)
    Salaryamount=models.IntegerField(default=0)
    Salaryteacher= models.ForeignKey(Instructor,on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Salaryteacher)


class StudetFee(models.Model):
    FeeId= models.AutoField(primary_key=True)
    IssueDate=models.DateTimeField(auto_now_add=True)
    FeeAmount=models.IntegerField(default=0)
    StudentId= models.ForeignKey(Student_Profile,on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.StudentId)
class serFee(serializers.ModelSerializer):
    class Meta:
        model =StudetFee
        fields= '__all__'
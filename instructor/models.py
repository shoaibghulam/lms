from django.db import models
from lmsapp.models import  User_Signup
from rest_framework import serializers
from UniversityApp.models import UniversityAccount , UniversityBranch

# Create your models here.

class teacher(models.Model):
    tid=models.AutoField(primary_key=True)
    uname=models.ForeignKey(User_Signup, on_delete=models.CASCADE)
    Name=models.CharField( max_length=255,default='')
    Occupation=models.CharField(max_length=255,default='')
    Company_Name=models.CharField(max_length=255,default='')
    Phone=models.CharField(max_length=15,default='')
    Personal_info=models.TextField(default='')
    Facebook=models.URLField(max_length=500,default='')
    Twitter=models.URLField(max_length=500,default='')
    Linkedin=models.URLField(max_length=500,default='')
    Google_Plus=models.URLField(max_length=500,default='')
    img=models.ImageField(upload_to='upload/',default="dummy.jpg")

class SerTeacher(serializers.ModelSerializer):
    class Meta:
        model= teacher
        fields=('tid','Name','Occupation','Company_Name','Phone','Personal_info','Facebook','Twitter','Linkedin','Google_Plus','img')

class CourseCategory(models.Model):
    catid= models.AutoField(primary_key=True)
    cattitle= models.CharField(max_length=255,default="")
    catdesct=models.CharField(max_length=255,default="")
    catimage= models.ImageField(upload_to='upload/',default="dummy.jpg")

    def __str__(self):
        return self.cattitle

class CourseLevel(models.Model):
    levelid= models.AutoField(primary_key=True)
    leveltitle= models.CharField(max_length=255,default="")

    def __str__(self):
        return self.leveltitle

class Course(models.Model):
    course_id=models.AutoField(primary_key=True)
    Course_title= models.CharField(max_length=255,default="")
    Course_description=models.TextField(default=0)
    Course_requirment=models.TextField(default=0)
    Course_start_date=models.DateTimeField(auto_now_add=True)
    Course_Price=models.TextField(default=0)
    Course_Duration=models.TextField(default=0)
    Course_Thumbnail=models.ImageField(upload_to='upload/',default="dummy.jpg")
    instructor_id=models.ForeignKey(User_Signup, on_delete=models.CASCADE)
    Course_category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    Course_Level=models.ForeignKey(CourseLevel, on_delete=models.CASCADE)
    def __str__(self):
        return self.Course_title
    


# videos for course
class videos(models.Model):
    vid=models.AutoField(primary_key=True)
    videoTitle=models.CharField(max_length=250, default='Video Title')
    videoFile=models.FileField(upload_to='videos/' ,default='test.jpg')
    courseId=models.ForeignKey(Course, on_delete=models.CASCADE)


    
# video seralizer
class serVideos(serializers.ModelSerializer):
    class Meta:
        model= videos
        fields= '__all__'
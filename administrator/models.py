from django.db import models
from datetime import datetime  
from faculty.models import Department,Instructor,Semester,Course
from student.models import Student_Profile,Student_Course
from rest_framework import serializers
from UniversityApp.models import UniversityAccount , UniversityBranch
FORMS =(
    ("facultyguidline","Faculty Guidline"),
    ("applicationform","Application Forms"),
    ("thesisguidline","Thesis Guidline"),
    ("placementforms","Placement Forms"),
    ("cacforms","Cac Forms"),
)
ROLES_CATEGORY =(
    ("assistantteacher","Assistant Teacher"),
    ("teacher","Teacher"),
    ("professor","Professor"),
    ("assistantprofessor","Assistant Professor"),
    ("hod","HOD"),
    ("registrar","Registrar"),
    ("dean","Dean"),
    ("viceChancelor","ViceChancelor"),
    ("librarian","Librarian"),
    
    
)
ACTIVE =(
    ("yes","YES"),
    ("no","NO"),
)
ROOMSTATUS=(
    ('Available','Available'),
    ('Booked','Booked'),
)
FOODMENU=(
    ('Tea','Hi Tea'),
    ('lunchmedium','Lunch Medium Course'),
    ('Lunchnormalcourse','Lunch Normal Course'),
)



class AcademicCalendarModel(models.Model):
    AcademicCalendarId= models.AutoField(primary_key=True)
    AcademicCalendarTitle=models.CharField(max_length=100, default="Title")
    AcademicCalendarDesc=models.TextField(max_length=400, default="Title")
    AcademicCalendarStartDate=models.DateTimeField(auto_now_add=True, blank=True)
    AcademicCalendarEndDate=models.DateTimeField(auto_now_add=True, blank=True)
    AcademicCalendarLocation=models.CharField(max_length=240, default="Address")
    Image=models.FileField(upload_to="job",default="Notdata")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.AcademicCalendarTitle
    

class FacultyCalendarModel(models.Model):
   FacultyCalendarId= models.AutoField(primary_key=True)
   FacultyCalendarTitle=models.CharField(max_length=100, default="Title")
   FacultyCalendarDesc=models.TextField(max_length=400, default="Title")
   FacultyCalendarStartDate=models.DateTimeField(auto_now_add=True, blank=True)
   FacultyCalendarEndDate=models.DateTimeField(auto_now_add=True, blank=True)
   FacultyCalendarLocation=models.CharField(max_length=240, default="Address")
   Image=models.FileField(upload_to="job",default="Notdata")
   Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
   uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
   branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
   def __str__(self):
        return self.FacultyCalendarTitle
    

class Form(models.Model):
    FormId=models.AutoField(primary_key=True)
    Formtitle=models.CharField(max_length=100,default="")
    FormFile=models.FileField(upload_to="forms",default="Notdata")
    FileCategory=models.CharField(max_length=100, choices=FORMS)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)

    def __str__(self):
        return self.Formtitle

class SerForm(serializers.ModelSerializer):
    class Meta:
        model= Form
        fields = '__all__'
    
class Admin_Notification(models.Model):
    NotificationId=models.AutoField(primary_key=True)
    NotificationTitle=models.CharField(max_length=100, default="Notification Title")
    NotificationDesc=models.TextField(max_length=200, default="Notification Description")
    Instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.NotificationTitle

class role(models.Model):
    roleid=models.AutoField(primary_key=True)
    category=models.CharField(max_length=100, choices=ROLES_CATEGORY)
    active=models.CharField(max_length=100, choices=ACTIVE)
    date=models.DateField(default=datetime.now(), blank=True)
    Instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
   
    def __str__(self):
        return self.active

class Serrole(serializers.ModelSerializer):
    class Meta:
        model= role
        fields=('roleid','category','active','date','Instructor_id','uniId','branchId')


# Room Reservation System Data Start

class Rooms(models.Model):
    RoomId=models.AutoField(primary_key=True)
    RoomName=models.CharField(max_length=100, default="Room Name")
    RoomCode=models.CharField(max_length=10, default="Room Code")
    RoomStatus=models.CharField(max_length=300 , choices=ROOMSTATUS , default="Available")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.RoomName

class Serroom(serializers.ModelSerializer):
    class Meta:
        model= Rooms
        fields=('RoomId','RoomName','RoomCode','RoomStatus','uniId','branchId')
    

class RoomReservation(models.Model):
    ReservationId=models.AutoField(primary_key=True)
    ReservationParticipants=models.CharField(max_length=200, default="Participants")
    ReservationComments=models.TextField(max_length=350, default="Comments")
    ReservationStartDate=models.DateField(default=datetime.now(), blank=True)
    ReservationStartTime=models.TimeField(default=datetime.now(), blank=True)
    ReservationEndDate=models.DateField(default=datetime.now(), blank=True)
    ReservationEndTime=models.TimeField(default=datetime.now(), blank=True)
    RoomId=models.ForeignKey(Rooms, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.ReservationParticipants
    

# Room Reservation System Data End

# Foood Reservation System Starte
class menu(models.Model):
    MenuId=models.AutoField(primary_key=True)
    MenuTitle=models.CharField(max_length=100, default="Menu Title")
    MenuType=models.CharField(max_length=50, choices=FOODMENU)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.MenuTitle

class Sermenu(serializers.ModelSerializer):
    class Meta:
        model= menu
        fields=('MenuId','MenuTitle','MenuType','uniId','branchId')
    
class MenuOrders(models.Model):
    OrderId=models.AutoField(primary_key=True)
    OrderParticipants=models.CharField(max_length=200, default="Participants")
    OrderComments=models.TextField(max_length=350, default="Comments")
    OrderList=models.TextField(max_length=450, default="Comments")
    OrderStartDate=models.DateField(default=datetime.now(), blank=True)
    OrderStartTime=models.TimeField(default=datetime.now(), blank=True)
    OrderEndDate=models.DateField(default=datetime.now(), blank=True)
    OrderEndTime=models.TimeField(default=datetime.now(), blank=True)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.OrderParticipants
    
   


    # Seralizer
class menuSer(serializers.ModelSerializer):
    class Meta:
        model = menu
        fields = '__all__'

# Foood Reservation System End

# Faculty Attendence system
class FacultyAttendence(models.Model):
    FacultyAttendenceId=models.AutoField(primary_key=True)
    FacultyAttendenceYear=models.TextField(max_length=50 , default="December")
    FacultyAttendenceMonth=models.TextField(max_length=50 , default="April")
    FacultyAttendencePresent=models.IntegerField(default=0)
    FacultyAttendenceAbsent=models.IntegerField(default=0)
    FacultyAttendenceTotal=models.FloatField(default=0.0)
    Instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.FacultyAttendenceId)
    

class Faculty_Evaluation_Report(models.Model):
    Faculty_Evaluation_Report_ID = models.AutoField(primary_key=True)
    Report_Name = models.CharField(max_length=200, default="Name")
    Report_File = models.FileField(upload_to="report",default="Notdata")
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Report_Name

class SerFaculty_Evaluation_Report(serializers.ModelSerializer):
    class Meta:
        model= Faculty_Evaluation_Report
        fields = '__all__'
    

class Semester_Schedule(models.Model):
    Semester_Schedule_Id = models.AutoField(primary_key=True)
    Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    Year = models.DateTimeField(default=datetime.now(), blank=True)
    Semester_Schedule_File=models.FileField(upload_to="semester_schedule",default="Notdata")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Semester_Schedule_Id)
    


class Exam_Schedule(models.Model):
    Exam_Schedule_Id = models.AutoField(primary_key=True)
    Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    Year = models.DateTimeField(default=datetime.now(), blank=True)
    Exam_Schedule_File=models.FileField(upload_to="semester_schedule",default="Notdata")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Exam_Schedule_Id)
    


class StudentAttendence(models.Model):
    StudentAttendenceId=models.AutoField(primary_key=True)
    StudentAttendenceYear=models.TextField(max_length=50 , default="December")
    StudentAttendenceMonth=models.TextField(max_length=50 , default="April")
    StudentAttendencePresent=models.IntegerField(default=0)
    StudentAttendenceAbsent=models.IntegerField(default=0)
    StudentAttendenceTotal=models.FloatField(default=0.0)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.StudentAttendenceId)
    
  
class onlinesurvey(models.Model):
    onlinesurvey_id=models.AutoField(primary_key=True)
    question_1=models.CharField(max_length=200,default="question1")
    question_2=models.CharField(max_length=200,default="question2")
    question_3=models.CharField(max_length=200,default="question3")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.onlinesurvey_id)
    
class Placement_Portal(models.Model):
    Placement_Portal_id=models.AutoField(primary_key=True)
    Job_Title = models.CharField(max_length=200,default="IT")
    Name_of_Organization = models.CharField(max_length=200,default="xyz")
    Company_Profile = models.CharField(max_length=200,default="Local")
    Employment_Type = models.CharField(max_length=200,default="xyz")
    Job_description = models.FileField(upload_to="job",default="Notdata")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Job_Title
    
class SerPlacement_Portal(serializers.ModelSerializer):
    class Meta:
        model = Placement_Portal
        fields = '__all__'
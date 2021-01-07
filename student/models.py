from django.db import models
from faculty.models import Course,Instructor
from datetime import datetime  
from rest_framework import serializers
from faculty.models import Semester,Department,Instructor,AssigmentModel,MidtermModel,FinalExamModel,CourseSeralizer,SerDepartment,onlinequiz
from UniversityApp.models import UniversityAccount , UniversityBranch

APPLICATIONSTATUS=(
    ('Pendding','Pendding'),
    ('Approved','Approved'),
    ('Cancel','Cancel'),
)
Category=(
    ("Section_a","Section_A"),
    ("Section_b","Section_B"),
    ("Section_c","Section_C"),
    ("Section_d","Section_D"),
    ("Section_e","Section_E"),
    ("Section_f","Section_F"),
)
class Batch(models.Model):
    Batch_id=models.AutoField(primary_key=True)
    Batch_Name=models.CharField(max_length=100,default="Batch_Name")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Batch_Name 

class Ser_Batch(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
class Section(models.Model):
    Section_id=models.AutoField(primary_key=True)
    Section_Name=models.CharField(max_length=100,choices=Category)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Section_id 
# Create your models here.
class Student_Signup(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,default="")
    email = models.CharField(max_length=100,default="")
    password = models.TextField(default='')
    verify=models.CharField(max_length=100,default="unverified") 
    role=models.CharField(max_length=50,default="null")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.username
    

class Student_Profile(models.Model):
    StudentId=models.AutoField(primary_key=True)
    First_name=models.CharField(max_length=100,default="First Name")
    Last_name=models.CharField(max_length=100,default="Last Name")
    ContactNo=models.CharField(max_length=100,default="Contact No")
    Address=models.CharField(max_length=150,default="Addresss")
    DOB=models.DateField()
    StudenBatch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    StudenShift=models.CharField(max_length=150,default="Morning")
    Profile=models.ImageField(upload_to="StudentProfile/",default="Thumb.jpg")
    User_id=models.ForeignKey(Student_Signup, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.First_name +" "+ self.Last_name



class SerStudent(serializers.ModelSerializer):
    class Meta:
        model= Student_Profile
        fields=('StudentId','First_name','Last_name','ContactNo','Address','DOB','StudenBatch','StudenShift')
    

class Application(models.Model):
    ApplicationId=models.AutoField(primary_key=True)
    ApplicationTitle=models.CharField(max_length=50, default="Reason Title")
    ApplicationMessage=models.TextField(max_length=350, default="Reason application")
    ApplicationAttachment=models.FileField(upload_to='ApplicationAttachment/',default='reason.pdf')
    ApplicationDate=models.DateTimeField(default=datetime.now(), blank=True)
    ApplicationStatus=models.CharField(max_length=30, default='Pendding')
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Instructor_id=models.ForeignKey(Instructor, on_delete=models.CASCADE)
    Techer_Reply=models.TextField(max_length=500,default="No Reply")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.ApplicationTitle
    
#student_Assignment serilize
class Ser_App(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'



class Student_Course(models.Model):
    Student_Course_ID = models.AutoField(primary_key=True)
    Student_ID = models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Courses = models.ManyToManyField(Course)
    Department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    StudenBatch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Student_Course_ID)
    

class Student_Query_Admin(models.Model):
    queryid=models.AutoField(primary_key=True)
    querytitle=models.CharField(max_length=50, default="Reason Title")
    querymessage=models.TextField(max_length=350, default="Reason query")
    querydate=models.DateTimeField(default=datetime.now(), blank=True)
    querystatus=models.CharField(max_length=30, default='Pendding')
    Student_ID = models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.querytitle
    

class Registration(models.Model):
    Student_Registration_Id = models.AutoField(primary_key=True)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Student_Registration_Code = models.CharField(max_length=50,default="000000")
    Student_Program = models.CharField(max_length=50,default="Program")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Student_Registration_Id)
    


class ScrunityForm(models.Model):
    Scrunity_Form_Id = models.AutoField(primary_key=True)
    Student_Name = models.CharField(max_length=100,default="Name")
    Program = models.CharField(max_length=100,default="Program")
    Registration_no = models.CharField(max_length=100,default="0000000")
    Date = models.DateTimeField(default=datetime.now(), blank=True)
    Scrunity_Rechecking = models.CharField(max_length=100,default="recheck")
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    Research_for_Evalution=models.CharField(max_length=300,default="evaluation")
    Voucher_Number = models.CharField(max_length=100,default="number")
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Student_Name
    

class Student_Survey(models.Model):
    Survey_id= models.AutoField(primary_key=True)
    question_1_Answer = models.CharField(max_length=15,default="agree")
    question_2_Answer = models.CharField(max_length=15,default="notagree")
    question_3_Answer = models.CharField(max_length=15,default="strongagree")
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Survey_id)
    

class MeetingAppointment(models.Model):
    Appointment_id=models.AutoField(primary_key=True)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    Department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    Student_ID = models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Semester_ID = models.ForeignKey(Semester, on_delete=models.CASCADE)
    Date=models.DateField()
    Time=models.TimeField()
    Techer_Reply=models.TextField(max_length=500,default="No Reply")
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Appointment_id)

class SerMeeting(serializers.ModelSerializer):
    class Meta:
        model = MeetingAppointment
        fields = '__all__'
    

    

class Job_Apply(models.Model):
    Job_Apply_id = models.AutoField(primary_key=True)
    Student_Name = models.CharField(max_length=100,default="Name")
    Program = models.CharField(max_length=100,default="Program")
    Job_Experirnce = models.TextField(max_length=10,default="0")
    Cv=models.FileField(upload_to="cv",default="Notdata")
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Student_Name
    


class Student_Submit_Evaluation(models.Model):
    Student_Submit_Evaluation_id = models.AutoField(primary_key=True)
    Student_Name = models.CharField(max_length=100,default="Name")
    Student_Program =  models.CharField(max_length=100,default="Program")
    Report_File = models.FileField(upload_to="report",default="Notdata")
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Student_Name
    


class Teacher_Appointment(models.Model):
    Teacher_Appointment_id= models.AutoField(primary_key=True)
    Student_Name= models.CharField(max_length=100,default="Name")
    Program= models.CharField(max_length=100,default="Program")
    Department= models.CharField(max_length=100,default="Department")
    Course= models.CharField(max_length=100,default="Course")
    Teacher= models.CharField(max_length=100,default="Teacher")
    Date_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.Student_Name
    


class Student_Assigment(models.Model):
    Student_Assigment_Id=models.AutoField(primary_key=True)
    Assigment_File=models.FileField(upload_to="studentassigment",default="Notdata")
    Date_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    roll=models.CharField(max_length=10,default="0")
    section=models.CharField(max_length=10,default="xyz")
    Teacher_Upload=models.FileField(upload_to="studentassigment",default="Notdata")
    Mark=models.CharField(max_length=20,default=0)
    Status=models.CharField(max_length=20,default="False")
    AsssigmentId=models.ForeignKey(AssigmentModel , on_delete=models.CASCADE,null=True,blank=True)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Student_Assigment_Id)


#student_Assignment serilize
class Ser_Assigment(serializers.ModelSerializer):
    class Meta:
        model = Student_Assigment
        fields = '__all__'


class Student_Midterm(models.Model):
    Student_Midterm_Id=models.AutoField(primary_key=True)
    Midterm_File=models.FileField(upload_to="studentassigment",default="Notdata")
    Date_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    roll=models.CharField(max_length=10,default="0")
    section=models.CharField(max_length=10,default="xyz")
    Teacher_Upload=models.FileField(upload_to="studentassigment",default="Notdata")
    Mark=models.CharField(max_length=20,default=0)
    Status=models.CharField(max_length=20,default="False")
    MidtermId=models.ForeignKey(MidtermModel , on_delete=models.CASCADE,null=True,blank=True)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Student_Midterm_Id)


#student_Assignment serilize
class Ser_Midterms(serializers.ModelSerializer):
    class Meta:
        model = Student_Midterm
        fields = '__all__'

class Student_FinalExam(models.Model):
    Student_FinalExam_Id=models.AutoField(primary_key=True)
    FinalExam_File=models.FileField(upload_to="studentassigment",default="Notdata")
    Date_Time = models.DateTimeField(default=datetime.now(), blank=True)
    Student_id=models.ForeignKey(Student_Profile, on_delete=models.CASCADE)
    Course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    roll=models.CharField(max_length=10,default="0")
    section=models.CharField(max_length=10,default="xyz")
    Teacher_Upload=models.FileField(upload_to="studentassigment",default="Notdata")
    Mark=models.CharField(max_length=20,default=0)
    Status=models.CharField(max_length=20,default="False")
    FinalExamId=models.ForeignKey(FinalExamModel , on_delete=models.CASCADE,null=True,blank=True)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Student_FinalExam_Id)


#student_Assignment serilize
class Ser_FinalExams(serializers.ModelSerializer):
    class Meta:
        model = Student_FinalExam
        fields = '__all__'
    
# seralizer data
class SerStudentCourse(serializers.ModelSerializer):
    StudenBatch=Ser_Batch(Batch , many=False, read_only=True)
    Courses=CourseSeralizer(Course , many=True, read_only=True)
    Department_id=SerDepartment(Department )

    class Meta:
        model = Student_Course
        fields = '__all__'

class SerStudentProfile(serializers.ModelSerializer):
    class Meta:
        model = Student_Profile
        fields = '__all__'


# Latest Model Create by shoaib ghulam 1/7/2021
class StudentQuizResult(models.Model):
    qId=models.AutoField(primary_key=True)
    studentId=models.ForeignKey(Student_Signup, on_delete=models.CASCADE)
    totalmarks=models.IntegerField()
    totalquestion=models.IntegerField()
    wrong=models.IntegerField()
    correct=models.IntegerField()
    score=models.IntegerField()
    quizId=models.ForeignKey(onlinequiz, on_delete=models.CASCADE)
    uniId=models.ForeignKey(UniversityAccount , on_delete=models.CASCADE)
    branchId=models.ForeignKey(UniversityBranch , on_delete=models.CASCADE)
    def __str__(self):
        return self.studentId
    
class serStudentQuizResult(serializers.ModelSerializer):
    class Meta:
        model = StudentQuizResult
        fields = '__all__'

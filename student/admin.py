from django.contrib import admin
from .models import Student_Signup,Student_Profile,Application,Student_Course,Student_Query_Admin,Registration,ScrunityForm,Student_Survey,MeetingAppointment,Job_Apply,Student_Submit_Evaluation,Student_Assigment,Batch,Section,Student_Midterm,Student_FinalExam,StudentQuizResult
# Register your models here.

# singup model list
class Student_Singup_Admin(admin.ModelAdmin):
    list_display=('username','email')

# Profile model list
class Student_Profile_Admin(admin.ModelAdmin):
    list_display=('First_name','Last_name','User_id')


class Student_Course_Admin(admin.ModelAdmin):
    list_display=('Student_Course_ID','Student_ID','Department_id','Semester_ID')


class Student_Query_Admin_Admin(admin.ModelAdmin):
    list_display=('queryid','querytitle','querymessage','querystatus','Student_ID','Course_id')

class Registration_Admin(admin.ModelAdmin):
    list_display=('Student_Registration_Id','Student_id','Student_Registration_Code','Student_Program')

class ScrunityForm_Admin(admin.ModelAdmin):
    list_display=('Scrunity_Form_Id','Student_Name','Program','Registration_no','Date')
    
class Job_Apply_Admin(admin.ModelAdmin):
    list_display=('Student_Name','Program','Job_Experirnce')


class Student_Survey_Admin(admin.ModelAdmin):
    list_display=('Survey_id','Student_id','question_1_Answer','question_2_Answer','question_3_Answer')


class MeetingAppointment_Admin(admin.ModelAdmin):
    list_display=('Appointment_id','Student_ID','Course_id','Department_id','Semester_ID')


class Student_Submit_Evaluation_Admin(admin.ModelAdmin):
    list_display=('Student_Submit_Evaluation_id','Student_Name','Student_Program','Student_id')


class Student_Assigment_Admin(admin.ModelAdmin):
    list_display=('Student_id','Course_id','Date_Time')

class Student_Midterm_Admin(admin.ModelAdmin):
    list_display=('Student_id','Course_id','Date_Time')

class Student_FinalExam_Admin(admin.ModelAdmin):
    list_display=('Student_id','Course_id','Date_Time')


#  student quiz
class StudentQuizResultModal(admin.ModelAdmin):
    list_display=('studentId','score','totalmarks')


# Student Application list
class Application_Admin(admin.ModelAdmin):
    list_display=('ApplicationTitle','ApplicationMessage','ApplicationAttachment','ApplicationDate','ApplicationStatus','Course_id','Student_id')

admin.site.register(Student_Signup,Student_Singup_Admin)
admin.site.register(Student_Profile,Student_Profile_Admin)
admin.site.register(Student_Course,Student_Course_Admin)
admin.site.register(Student_Query_Admin,Student_Query_Admin_Admin)


admin.site.register(Application,Application_Admin)
admin.site.register(Registration,Registration_Admin)
admin.site.register(ScrunityForm,ScrunityForm_Admin)
admin.site.register(Student_Survey,Student_Survey_Admin)
admin.site.register(MeetingAppointment,MeetingAppointment_Admin)
admin.site.register(Job_Apply,Job_Apply_Admin)
admin.site.register(Student_Submit_Evaluation,Student_Submit_Evaluation_Admin)
admin.site.register(Student_Assigment,Student_Assigment_Admin)
admin.site.register(Section)
admin.site.register(Batch)
admin.site.register(Student_FinalExam,Student_FinalExam_Admin)
admin.site.register(Student_Midterm,Student_Midterm_Admin)
admin.site.register(StudentQuizResult,StudentQuizResultModal)

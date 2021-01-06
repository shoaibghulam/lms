from django.contrib import admin
from .models import Instructor,Department,Course,User_Signup,Materialclass,AssigmentModel,NotificationModel,Teacher_syllabus,TeacherApplication,User_Stories,Query_Admin,CourseVideos,Faculty_Development,Faculty_Evaluation,Exam_Result,Semester,onlinequiz,MidtermModel,FinalExamModel,quaizsheet
# Dashboard Labeling
class quaizsheetView(admin.ModelAdmin):
    list_display=('question','a1','a2','a3','a4','currectAnswse','quizid')

class InstructorAdmin(admin.ModelAdmin):
    list_display=('First_Name','Last_Name','Gender','Phone_Number')

class DepartmentAdmin(admin.ModelAdmin):
    list_display=('Did','Department_name')

class CourseAdmin(admin.ModelAdmin):
    list_display=('Cid','Course_name','Issue_Date','Instructor_id','Semester_id')

class MaterialclassAdmin(admin.ModelAdmin):
    list_display=('Title','Category','Course_id','Instructor_id')


class AssigmentAdmin(admin.ModelAdmin):
    list_display=('AssigmentTitle','Course_id','Instructor_id')

class MidtermModelAdmin(admin.ModelAdmin):
    list_display=('MidtermTitle','Course_id','Instructor_id')

class FinalExamModelAdmin(admin.ModelAdmin):
    list_display=('FinalExamTitle','Course_id','Instructor_id')

class NotificationModelAdmin(admin.ModelAdmin):
    list_display=('NotificationTitle','Category','Course_id','Instructor_id')

class User_SignupAdmin(admin.ModelAdmin):
    list_display=('username','email','role')

class syllabusAdmin(admin.ModelAdmin):
    list_display=('Instructor_id','Department_id','Course_id','semester')
class User_StorieAdmin(admin.ModelAdmin):
    list_display=('storyid','I_want_to','Category','Instructor_id')
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display=('ApplicationId','ApplicationTitle','ApplicationDate','ApplicationStatus','Instructor_id')
class Query_AdminAdmin(admin.ModelAdmin):
    list_display=('queryid','querytitle','querydate','querystatus','Instructor_id')

class CourseVideosAdmin(admin.ModelAdmin):
    list_display=('VideoId','VideoTitle','CourseId','InstructerId')

class Semester_Admin(admin.ModelAdmin):
    list_display=('SamesterId','Samester_Name','Samester_Code','Samester_Year')
class onlinequiz_Admin(admin.ModelAdmin):
    list_display=('semester','Course_id','Department_id','Instructor_id','quizlink')

class Faculty_DevelopmentAdmin(admin.ModelAdmin):
    list_display=('Faculty_Development_ID','Name','Department','Instructor_id')

class Faculty_Evaluation_Admin(admin.ModelAdmin):
    list_display=('Faculty_Evaluation_ID','Report_Name','Report_File','Department_id','Course_id')

class Exam_Result_Admin(admin.ModelAdmin):
    list_display=('Exam_Result_id','Course_id','Project_Marks','Quiz_Assignment_Marks','Midterm_Marks','Total_Marks','Final_Marks','InstructerId','Department_id')



admin.site.register(CourseVideos,CourseVideosAdmin)
admin.site.register(Instructor,InstructorAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(User_Signup)
admin.site.register(Materialclass,MaterialclassAdmin)
admin.site.register(AssigmentModel,AssigmentAdmin)
admin.site.register(NotificationModel,NotificationModelAdmin)
admin.site.register(Teacher_syllabus,syllabusAdmin)
admin.site.register(TeacherApplication,TeacherApplicationAdmin)
admin.site.register(User_Stories,User_StorieAdmin)
admin.site.register(Query_Admin,Query_AdminAdmin)
admin.site.register(Faculty_Development,Faculty_DevelopmentAdmin)
admin.site.register(Faculty_Evaluation,Faculty_Evaluation_Admin)
admin.site.register(Exam_Result,Exam_Result_Admin)
admin.site.register(Semester,Semester_Admin)
admin.site.register(onlinequiz,onlinequiz_Admin)
admin.site.register(MidtermModel,MidtermModelAdmin)
admin.site.register(FinalExamModel,FinalExamModelAdmin)
admin.site.register(quaizsheet,quaizsheetView)

from django.contrib import admin

from .models import AcademicCalendarModel,FacultyCalendarModel,Form,Admin_Notification,role,Rooms,RoomReservation,menu,MenuOrders,FacultyAttendence,Faculty_Evaluation_Report,Semester_Schedule,Exam_Schedule,StudentAttendence,onlinesurvey,Placement_Portal

# Register your models here.
# Profile Samester list


class AcademicCalendarModel_Admin(admin.ModelAdmin):
    list_display=('AcademicCalendarId','AcademicCalendarTitle','AcademicCalendarStartDate','AcademicCalendarEndDate','AcademicCalendarLocation')


class FacultyCalendarModel_Admin(admin.ModelAdmin):
    list_display=('FacultyCalendarId','FacultyCalendarTitle','FacultyCalendarStartDate','FacultyCalendarEndDate','FacultyCalendarLocation')

class Form_Admin(admin.ModelAdmin):
    list_display=('FormId','FormFile','FileCategory')

class Admin_Notification_Admin(admin.ModelAdmin):
    list_display=('NotificationTitle','NotificationDesc','Instructor_id','Department_id')
class role_Admin(admin.ModelAdmin):
    list_display=('Instructor_id','category','active','date')
    

#
# Room Reservation System Data Start
class RoomsAdmin(admin.ModelAdmin):
    list_display=('RoomName','RoomStatus','RoomCode')

class RoomReservationAdmin(admin.ModelAdmin):
    list_display=('ReservationId','ReservationParticipants','ReservationStartDate','ReservationStartTime','ReservationEndTime','RoomId')

admin.site.register(Rooms,RoomsAdmin)
admin.site.register(RoomReservation, RoomReservationAdmin)

# Room Reservation System Data End

# Faculty Attendence system Start
class FacultyAttendenceAdmin(admin.ModelAdmin):
    list_display=('FacultyAttendenceId','FacultyAttendenceYear','FacultyAttendenceMonth','FacultyAttendencePresent','FacultyAttendenceAbsent','FacultyAttendenceTotal','Instructor_id')
class StudentAttendence_Admin(admin.ModelAdmin):
    list_display=('StudentAttendenceId','StudentAttendenceYear','StudentAttendenceMonth','StudentAttendencePresent','StudentAttendenceAbsent','StudentAttendenceTotal','Student_id','Department_id')
    
admin.site.register(FacultyAttendence, FacultyAttendenceAdmin)


# Faculty Attendence system End

# Order Reservation System Start
class menuAdmin(admin.ModelAdmin):
    list_display=('MenuId','MenuTitle','MenuType')

class OrdermenuAdmin(admin.ModelAdmin):
    list_display=('OrderId','OrderList','OrderStartDate','OrderStartTime','OrderEndTime')

class Faculty_Evaluation_Report_Admin(admin.ModelAdmin):
    list_display=('Faculty_Evaluation_Report_ID','Report_Name','Report_File','Department_id')

class Semester_Schedule_Admin(admin.ModelAdmin):
    list_display=('Semester_Schedule_Id','Semester_ID','Department_id','Year')


class Exam_Schedule_Admin(admin.ModelAdmin):
    list_display=('Exam_Schedule_Id','Semester_ID','Department_id','Year')

class onlinesurvey_Admin(admin.ModelAdmin):
    list_display=('onlinesurvey_id','question_1')

class Placement_Portal_Admin(admin.ModelAdmin):
    list_display=('Placement_Portal_id','Job_Title','Name_of_Organization','Company_Profile','Employment_Type')


admin.site.register(menu,menuAdmin)
admin.site.register(MenuOrders,OrdermenuAdmin)

# Order Reservation System End



admin.site.register(Form,Form_Admin)
admin.site.register(AcademicCalendarModel,AcademicCalendarModel_Admin)
admin.site.register(FacultyCalendarModel,FacultyCalendarModel_Admin)
admin.site.register(Admin_Notification,Admin_Notification_Admin)
admin.site.register(role,role_Admin)
admin.site.register(Faculty_Evaluation_Report,Faculty_Evaluation_Report_Admin)
admin.site.register(Semester_Schedule,Semester_Schedule_Admin)
admin.site.register(Exam_Schedule,Exam_Schedule_Admin)
admin.site.register(StudentAttendence,StudentAttendence_Admin)
admin.site.register(onlinesurvey,onlinesurvey_Admin)
admin.site.register(Placement_Portal,Placement_Portal_Admin)


admin.site.site_header = 'Digital learning System Admin Panel'
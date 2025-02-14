from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.fdashboard,name='fdashboard'),
    path('showstudentassignment', views.showstudentassignment,name='showstudentassignment'),
    path('semesterschedule', views.semesterschedule,name='semesterschedule'),
    path('formguidline', views.formguidline,name='formguidline'),
    path('library', views.library,name='library'),
    path('digitallibrary', views.digitallibrary,name='digitallibrary'),
    path('suggestiondigitallibrary', views.suggestiondigitallibrary,name='suggestiondigitallibrary'),
    path('Phddigitallibrary', views.Phddigitallibrary,name='Phddigitallibrary'),
    path('suggesPhddigitallibrary', views.suggesPhddigitallibrary,name='suggesPhddigitallibrary'),
    path('academiccalendar', views.academiccalendar,name='academiccalendar'),
    path('facultycalendar', views.facultycalendar,name='facultycalendar'),
    path('examresult', views.examresult,name='examresult'),
    path('facultyevaluation', views.facultyevaluation,name='facultyevaluation'),
    path('attendance', views.attendance,name='attendance'),
    path('userstories', views.userstories,name='userstories'),
    path('facultyform', views.facultyform,name='facultyform'),
    path('coursefile', views.coursefile,name='coursefile'),
    path('roomreservation', views.roomreservation,name='roomreservation'),
    path('foodreservation', views.foodreservation,name='foodreservation'),
    path('onlinelecture', views.onlinelecture,name='onlinelecture'),
    path('facultyattendance', views.facultyattendance,name='facultyattendance'),
    path('fvledashboard', views.fvledashboard,name='fvledashboard'),
    path('email', views.email,name='email'),
    path('myclass', views.myclass,name='myclass'),
    path('onlinequery', views.onlinequery,name='onlinequery'),
    path('createquery', views.createquery,name='createquery'),
    # path('mynotification', views.mynotification,name='mynotification'),
    path('myroles', views.myroles,name='myroles'),
    path('classmaterial', views.classmaterial,name='classmaterial'),
    path('onlinelecture', views.onlinelecture,name='onlinelecture'),
    path('onlinebook', views.onlinebook,name='onlinebook'),
    path('onlinequiz', views.Onlinequiz,name='onlinequiz'),
    path('assignment', views.assignment,name='assignment'),
    path('mygrade', views.mygrade,name='mygrade'),
    path('notification', views.notification,name='notification'),
    path('createnotification', views.createnotification,name='createnotification'),
    path('application', views.application,name='application'),
    path('createapplication', views.createapplication,name='createapplication'),
    path('liststudent', views.liststudent,name='liststudent'),
    path('creategradebook', views.creategradebook,name='creategradebook'),
    path('createprogramnoti', views.createprogramnoti,name='createprogramnoti'),
    path('classnotification', views.classnotification,name='classnotification'),
    path('syllabus', views.syllabus,name='syllabus'),
    path('createsyllabus', views.createsyllabus,name='createsyllabus'),
    path('notification', views.notification,name='notification'),
    path('app', views.app,name='app'),
    path('showstudentapp', views.showstudentapp,name='showstudentapp'),

    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="login"),
    path('verification/<str:verification>/<str:username>',views.verification, name='verification'),
    path('forget/<str:verification>/<str:username>',views.forget, name='forget'),
    path('forgetrequest',views.forgetrequest,name="frequest"),
    path('logout',views.logout,name="logout"),
    path('accounts/',include('allauth.urls')),
    path('becometeacher',views.becometeacher,name="becometeacher"),
    path('showteacher',views.showteacher,name="showteacher"),
    path('editinstructor',views.editinstructor,name="editinstructor"),
    path('RoomReservationinsert',views.RoomReservationinsert,name="RoomReservationinsert"),
    path('menudata',views.menudata,name="menudata"),
    path('showvideo',views.showvideo,name="showvideo"),
    path('AddVideos',views.AddVideos,name="AddVideos"),
    path('examschedule',views.examschedule,name="examschedule"),
    path('resultentry',views.resultentry,name="resultentry"),
    path('studentassignment',views.studentassignment,name="studentassignment"),
    path('videocall',views.videocall,name="videocall"),
    path('onlineclass',views.onlineclass,name="onlineclass"),
    path('Appointment',views.Appointment,name="Appointment"),
    path('ShowAppointment',views.ShowAppointment,name="ShowAppointment"),

    path('chat',views.chat,name="chat"),
    # path('testpass',views.testpass,name="testpass"),
    path('deletequiz/<int:id>',views.deletequiz,name="deletequiz"),
    path('IndividualMarksUpload',views.IndividualMarksUpload,name="IndividualMarksUpload"),
    path('editexamresult',views.editexamresult,name="editexamresult"),
    path('ShowStudentMarks',views.ShowStudentMarks,name="ShowStudentMarks"),

    path('midterm',views.midterm,name="midterm"),
    path('studentmidterm',views.studentmidterm,name="studentmidterm"),
    path('finalexam',views.finalexam,name="finalexam"),
    path('studentfinalexam',views.studentfinalexam,name="studentfinalexam"),
    path('showmidterm',views.showmidterm,name="showmidterm"),
    path('showfinalexam',views.showfinalexam,name="showfinalexam"),
    path('lockresult',views.lockresult,name="lockresult"),
# blow url defined by shoaib ghulam
    path('meeting', views.classmeetingdata,name="meeting"),
    path('meetingnotification', views.meetingnotification,name="meetingnotification"),
    path('onlineclass', views.onlineclass,name="onlineclassteacher"),
    path('coursedata', views.coursedatafatching,name="coursedata"),
    path('startmeeting', views.startmeeting,name="startmeeting"),
    path('meetingdata', views.meetingdata,name="meetingdata"),
    path('addStudentatten',views.addStudentatten,name="addStudentatten"),
    path('studentAttendanceData',views.studentAttendanceData,name="studentAttendanceData"),
    path('quizsheet/<int:qid>',views.quizsheet,name="quizsheet"),
    path('quizsheetsave',views.quizsheetsave,name="quizsheetsave"),
    path('quizstatus/<int:id>/<str:status>',views.quizstatus,name="quizsheetsave"),





    
    
    
    
   
]


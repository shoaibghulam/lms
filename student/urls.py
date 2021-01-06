from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.studentdashboard,name='studentdashboard'),
    path('examschedule', views.examschedule,name='examschedule'),
    path('examresultstudent', views.examresultstudent,name='examresultstudent'),
    path('registration', views.registration,name='registration'),
    path('transcript', views.transcript,name='transcript'),
    path('studentcalendar', views.studentcalendar,name='studentcalendar'),
    path('facultyevaluations', views.facultyevaluations,name='facultyevaluations'),
    path('studentattendance', views.studentattendance,name='studentattendance'),
    path('Scrunityform', views.Scrunityform,name='Scrunityform'),
    path('semesterschedule', views.semesterschedule,name='semesterschedule'),
    path('curriculum', views.curriculum,name='curriculum'),
    path('formguidline', views.formguidline,name='formguidline'),
    path('survey', views.survey,name='survey'),
    path('events', views.events,name='events'),
    path('showevents', views.showevents,name='showevents'),
    path('library', views.library,name='library'),
    path('digitallibrary', views.digitallibrary,name='digitallibrary'),
    path('suggestiondigitallibrary', views.suggestiondigitallibrary,name='suggestiondigitallibrary'),
    path('Phddigitallibrary', views.Phddigitallibrary,name='Phddigitallibrary'),
    path('suggesPhddigitallibrary', views.suggesPhddigitallibrary,name='suggesPhddigitallibrary'),
    path('placement', views.placement,name='placement'),
    path('onlinelecture', views.onlinelecture,name='onlinelecture'),
    path('fvledashboard', views.fvledashboard,name='fvledashboard'),
    path('email', views.email,name='email'),
    path('myclass', views.myclass,name='myclass'),
    path('classmaterial', views.classmaterial,name='classmaterial'),
    path('onlinequiz', views.Onlinequiz,name='onlinequiz'),
    path('assignments', views.assignments,name='assignments'),
    path('mygrade', views.mygrade,name='mygrade'),
    path('notification', views.notification,name='notification'),
    path('application', views.application,name='application'),
    path('teacherreply', views.teacherreply,name='teacherreply'),
    path('mynotification', views.mynotification,name='mynotification'),
    path('application', views.application,name='application'),
    path('application', views.application,name='application'),
    path('createapplication', views.createapplication,name='createapplication'),
    path('onlinebook', views.onlinebook,name='onlinebook'),
    path('onlinequery', views.onlinequery,name='onlinequery'),
    path('createquery', views.createquery,name='createquery'),
    path('myroles', views.myroles,name='myroles'),
    path('programnotification', views.programnotification,name='programnotification'),
    path('secnotification', views.secnotification,name='secnotification'),
    path('allnotification', views.allnotification,name='allnotification'),
    path('studentprofile', views.studentprofile,name='studentprofile'),
    path('showstudent', views.showstudent,name='showstudent'),
    path('editstudent', views.editstudent,name='editstudent'),
    path('jobapply', views.jobapply,name='jobapply'),
    path('submitreport', views.submitreport,name='submitreport'),
    path('logout',views.logout,name="login"),
    path('logout',views.logout,name="login"),
    path('submitassignment', views.submitassignment,name='submitassignment'),
    path('videocall',views.videocall,name="videocall"),
    path('onlineclass',views.onlineclass,name="onlineclass"),
   
    path('chat',views.chat,name="chat"),
    path('startquiz/<int:id>',views.startquiz,name="startquiz"),
    path('video/<int:id>',views.video,name="video"),
    path('showstudentAssignment',views.showstudentAssignment,name="showstudentAssignment"),

    path('midterm',views.midterm,name="midterm"),
    path('showmidterm',views.showmidterm,name="showmidterm"),
    path('finalexam',views.finalexam,name="finalexam"),
    path('showfinalexam',views.showfinalexam,name="showfinalexam"),
    path('submitmidterm',views.submitmidterm,name="submitmidterm"),
    path('submitfinalexam',views.submitfinalexam,name="submitfinalexam"),
    # urls created  by shoaib ghulam
    path('studentmeeting',views.studentmeeting,name="studentmeeting"),
    path('meeting',views.meeting,name="joinmeetingstudent"),
 
    
  

   
   
   
]



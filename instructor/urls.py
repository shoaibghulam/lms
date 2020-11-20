from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('mycourses', views.mycourses,name='mycourses'),
    path('myorder', views.myorder,name='myorder'),
    path('mymessages', views.mymessages,name='mymessages'),
    path('myreview', views.myreview,name='myreview'),
    path('mybookmarks', views.mybookmarks,name='mybookmarks'),
    path('mylisting', views.mylisting,name='mylisting'),
    path('becomeinstructor', views.becomeinstructor,name='becomeinstructor'),
    path('showinstructor', views.showinstructor,name='showinstructor'),
    path('editinstructor', views.editinstructor,name='editinstructor'),
    path('uploadvideo', views.uploadvideo,name='uploadvideo'),
    path('insertvideo', views.insertvideo,name='insertvideo'),
    path('videosview', views.videosview,name='videosview'),

   
]
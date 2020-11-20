from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('users', views.users,name='users'),
    path('sendmsg', views.sendmsg,name='sendmsg'),
    path('oldmessages', views.oldmessages,name='oldmessages'),


   ]
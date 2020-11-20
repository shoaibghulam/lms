from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.event,name='event'),
    path('eventinfo/<int:id>', views.eventinfo,name='eventinfo'),
   

   ]
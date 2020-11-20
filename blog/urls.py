from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.blog1,name='blog'),
    path('<str:slug>', views.blogPost, name='blogPost'),

   ]
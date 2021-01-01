from django.urls import path , include
from . import views

urlpatterns = [
   path('',views.Homepage.as_view(),name="financehomepage"),
   path('salary',views.TeacherSalary.as_view(),name="salary"),
   path('fees',views.StudentFees.as_view(),name="fees"),
   path('checkstudent',views.CheckStudent.as_view(),name="checkstudent"),
   path('loginverify',views.LoginVerify.as_view(),name="loginverify"),
  
   

   ]
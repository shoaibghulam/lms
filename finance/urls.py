from django.urls import path , include
from finance.views import *

urlpatterns = [
   path('',Homepage.as_view(),name="financehomepage"),
   path('salary',TeacherSalaryView.as_view(),name="salary"),
   path('fees',StudentFees.as_view(),name="fees"),
   path('checkstudent',CheckStudent.as_view(),name="checkstudent"),
   path('loginverify',LoginVerify.as_view(),name="loginverify"),
   path('StudentFeeUpdate',StudentFeeUpdate.as_view(),name="StudentFeeUpdate"),
   path('setudentfeedelete',SetudentFeeDelete.as_view(),name="setudentfeedelete"),
   path('queryData',queryData.as_view(),name="queryData"),
   path('CheckTeacher',CheckTeacher.as_view(),name="CheckTeacher"),
   path('TeacerSalaryUpdate',TeacerSalaryUpdate.as_view(),name="TeacerSalaryUpdate"),
   path('TeacherSalaryDelete',TeacherSalaryDelete.as_view(),name="TeacherSalaryDelete"),
   path('queryDataSalary',queryDataSalary.as_view(),name="queryDataSalary"),
   path('LogoutClass',LogoutClass.as_view(),name="LogoutClass"),
  
   

   ]
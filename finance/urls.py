from django.urls import path , include
from finance.views import *

urlpatterns = [
   path('',Homepage.as_view(),name="financehomepage"),
   path('salary',TeacherSalary.as_view(),name="salary"),
   path('fees',StudentFees.as_view(),name="fees"),
   path('checkstudent',CheckStudent.as_view(),name="checkstudent"),
   path('loginverify',LoginVerify.as_view(),name="loginverify"),
   path('StudentFeeUpdate',StudentFeeUpdate.as_view(),name="StudentFeeUpdate"),
   path('setudentfeedelete',SetudentFeeDelete.as_view(),name="setudentfeedelete"),
   path('queryData',queryData.as_view(),name="queryData"),
  
   

   ]
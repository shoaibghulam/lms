from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('contact', views.contact,name='contact'),
    # path('pagecoursev1', views.pagecoursev1,name='pagecoursev1'),
    path('pagecoursev2', views.pagecoursev2,name='pagecoursev2'),
    # path('pagecoursev3', views.pagecoursev3,name='pagecoursev3'),
    path('instructor', views.instructor,name='instructor'),
    path('instructorsingle', views.instructorsingle,name='instructorsingle'),
    # path('event', views.event,name='event'),
    # path('event1', views.event1,name='event1'),
    path('coursev2',views.coursev2,name="coursev2"),
    path('coursev1',views.coursev1,name="coursev1"),
    path('coursev3',views.coursev3,name="coursev3"),
    path('blog1',views.blog1,name="blog1"),
    path('blog2',views.blog2,name="blog2"),
    path('blog3',views.blog3,name="blog3"),
    path('singlepost',views.single_post,name="singlepost"),
    path('signup',views.signup,name="signup"),
    # path('login',views.login,name="login"),
    # path('logout',views.logout,name="login"),
    path('logoutfaculty',views.logoutfaculty,name="logoutfaculty"),
    
    path('verification/<str:verification>/<str:username>',views.verification, name='verification'),
    #path('forget', views.forgett,name='forget'),
    path('forget/<str:verification>/<str:username>',views.forget, name='forget'),
    path('forgetrequest',views.forgetrequest,name="frequest"),
    path('logout',views.logout,name="logout"),
    path('accounts/',include('allauth.urls')),
    path('google', views.base, name='google'),
   # path('<str:slug>',views.error, name='error'),
   

    path('studentlogin/<str:name>/<str:username>', views.studentlogin,name="studentlogin"),
    path('Facultylogin/<str:name>/<str:username>', views.Facultylogin,name="Facultylogin"),
   






]
from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index,name="superadmin"),
    path('university', views.university,name="university"),
    path('universitybranch', views.universitybranch,name="universitybranch"),
    path('universitypakage', views.universitypakage,name="universitypakage"),
    path('profile', views.Profile,name="profile"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('insert', views.insert,name="insert"),
    path('show', views.show,name="show"),
    path('uniadd', views.uniadd,name="uniadd"),
    path('unishow', views.unishow,name="unishow"),
    path('delete', views.delete,name="delete"),
    path('deleteuni', views.deleteuni,name="deleteuni"),
    path('update', views.update,name="update"),
    path('updateuni', views.updateuni,name="updateuni"),
    path('profileupdate', views.profileupdate,name="profileupdate"),
    path('activeuni', views.activeuni,name="activeuni"),
    path('disableunistatus', views.disableunistatus,name="disableunistatus"),
    path('showpackagedetail', views.showpackagedetail,name="showpackagedetail"),
    path('disableuni', views.disableuni,name="disableuni"),
    path('activeunistatus', views.activeunistatus,name="activeunistatus"),
    path('branchdata', views.branchdata,name="branchdata"),
    path('Count', views.Count,name="Count"),


   ]
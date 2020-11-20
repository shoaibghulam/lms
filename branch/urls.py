from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.index,name="branch"),
    path('universitybranch', views.universitybranch,name="universitybranch"),
    path('profile', views.profile,name="profile"),
    path('profileshow', views.profileshow,name="profileshow"),
    path('login', views.login,name="login"),
    path('logout', views.logout,name="logout"),
    path('addbranch', views.addbranch,name="addbranch"),
    path('deletebranch/<int:id>', views.deletebranch,name="deletebranch"),
    path('editbranch', views.editbranch,name="editbranch"),
    path('show', views.show,name="show"),
    # path('uniadd', views.uniadd,name="uniadd"),
    # path('unishow', views.unishow,name="unishow"),
    # path('delete', views.delete,name="delete"),
    # path('deleteuni', views.deleteuni,name="deleteuni"),
    # path('update', views.update,name="update"),
    # path('updateuni', views.updateuni,name="updateuni"),
    # path('profileupdate', views.profileupdate,name="profileupdate"),
    # path('activeuni', views.activeuni,name="activeuni"),
    # path('disableunistatus', views.disableunistatus,name="disableunistatus"),
    # path('showpackagedetail', views.showpackagedetail,name="showpackagedetail"),
    # path('disableuni', views.disableuni,name="disableuni"),
    # path('activeunistatus', views.activeunistatus,name="activeunistatus"),


   ]
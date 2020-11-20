from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact,User_Signup

# Register your models here.
admin.site.register(Contact)
admin.site.register(User_Signup)
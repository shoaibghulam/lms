from django.contrib import admin
from .models import FianceUser,TeacherSalary,StudetFee


class FianceUserModel(admin.ModelAdmin):
    list_display=('Fid','FirstName','LastName','Email','uniId','branchId')

class SalaryModel(admin.ModelAdmin):
    list_display=('SalaryId','IssueDate','Salaryamount','Salaryteacher','uniId','branchId')

class FeeModel(admin.ModelAdmin):
    list_display=('FeeId','IssueDate','FeeAmount','StudentId','uniId','branchId')

admin.site.register(FianceUser,FianceUserModel)
admin.site.register(TeacherSalary,SalaryModel)
admin.site.register(StudetFee,FeeModel)


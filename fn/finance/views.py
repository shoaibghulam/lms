from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.contrib import messages
from UniversityApp.models import UniversityAccount,UniversityBranch
from .models import  FianceUser,StudetFee,serFee,TeacherSalary,serSalary
from student.models import Student_Profile,SerStudent
from faculty.models import Instructor ,SerTeacher
from django.db.models import Q
import json
from datetime import datetime
from django.db.models import Sum



# Create your views here.

# unisession for instance
def unisession(request):
    unidata=UniversityAccount.objects.get(UniId=request.session['financeuni'])
    return unidata
# branch session for instance
def branchsession(request):
    branchdata=UniversityBranch.objects.get(BranchId=request.session['financebranch'])
    return branchdata
# Finance verification section code start
class LoginVerify(View):
    def post(self,request):
        try:
            uniid= unisession(request)
        
            branchid= branchsession(request)
            email= request.POST['email']
            password= request.POST['pass']
        
            data=FianceUser.objects.get(Email=email, uniId=uniid.UniId, branchId=branchid.BranchId)
            if data.Password== password:
                request.session['financeid']=data.Fid
                return redirect('/finance/')
                # return HttpResponse("heol")
              
            else:
                messages.error(request,"Please Enter Correct Username and Password")
                return redirect('/finance/'+uniid.UniUsername+"/"+branchid.BranchUsername)

          
        except :
            messages.error(request,"Please Enter Correct Username and Password")
            return redirect('/finance/'+uniid.UniUsername+"/"+branchid.BranchUsername)
    def get(self , request):
            messages.error(request,"Access Denied")
            return redirect('/finance/'+uniid.UniUsername+"/"+branchid.BranchUsername)
# Finance verification section code end



class Homepage(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')
        
        salary=TeacherSalary.objects.aggregate(Sum('Salaryamount'))
        fee=StudetFee.objects.aggregate(Sum('FeeAmount'))
        dataset={
            'salary':salary,
            'fee':fee,
        }

      
        
        return render(request,'finance/home.html',dataset)
        # return HttpResponse("working")

class TeacherSalaryView(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')


        teacherdata= TeacherSalary.objects.filter(uniId=request.session['financeuni'],branchId=request.session['financebranch']).order_by('-pk')
       
        dataSet={
            'data':teacherdata
        }
        return render(request,'finance/salary.html',dataSet)
        # return HttpResponse("working")
    def post(self, request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        sid = request.POST['tacherid']
        amount = request.POST['salary']
        tdata= Instructor.objects.get(pk=sid)
        print(tdata)
        salarydata=TeacherSalary(Salaryteacher=tdata,Salaryamount=amount,uniId=UniversityAccount.objects.get(UniId=request.session['financeuni']),branchId=UniversityBranch.objects.get(BranchId=request.session['financebranch']))
        salarydata.save()
        return redirect('/finance/salary')
       

class StudentFees(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')
        
        data= StudetFee.objects.filter(uniId=request.session['financeuni'],branchId=request.session['financebranch']).order_by('-pk')
        dataSet={
            'data':data
        }
        return render(request,'finance/fees.html',dataSet)
    def post(self, request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        sid = request.POST['studentid']
        amount = request.POST['fees']
        sdata= Student_Profile.objects.get(pk=sid)
        feesdata=StudetFee(StudentId=sdata,FeeAmount=amount,uniId=UniversityAccount.objects.get(UniId=request.session['financeuni']),branchId=UniversityBranch.objects.get(BranchId=request.session['financebranch']))
        feesdata.save()
        return redirect('/finance/fees')
class CheckStudent(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')
       
        try:
            id=request.GET['id']
            data=Student_Profile.objects.filter(Q(StudentId=id)|Q(User_id=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
            checkdata=StudetFee.objects.filter(StudentId=id)
            currentdate= datetime.now()
            dbdate=checkdata[0].IssueDate
            # print("dbmonth",dbdate.month)
            # print("db year",dbdate.year)
            # print("current month",currentdate.month)
            # print("current year",currentdate.year)
            if dbdate.month == currentdate.month:
                return HttpResponse("paid")
            else:
                data=Student_Profile.objects.get(Q(StudentId=id)|Q(User_id=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
                serdata=SerStudent(data, many=False)
                return HttpResponse(json.dumps(serdata.data))
            
        except:
            try:
                # print("meine")
                id=request.GET['id']
                data=Student_Profile.objects.get(Q(StudentId=id)|Q(User_id=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
                serdata=SerStudent(data, many=False)
                return HttpResponse(json.dumps(serdata.data))
            except Exception:
                return HttpResponse("not")
      
class SetudentFeeDelete(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')


        id=request.GET.get('id')
        data= StudetFee.objects.get(FeeId=id,uniId=request.session['financeuni'],branchId=request.session['financebranch'])
        print(request.session['financebranch'])
        data.delete()
        messages.error(request,"Record has been Deleted")
        return redirect('/finance/fees')
class StudentFeeUpdate(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        id= request.GET['id']
        data=StudetFee.objects.get(FeeId=id,uniId=request.session['financeuni'],branchId=request.session['financebranch'])
        print(request.session['financebranch'])
        serdata=serFee(data, many=False)
        return HttpResponse(json.dumps(serdata.data))
    
    def post(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        id=request.POST['sid']
        amount=request.POST['fee']
        data=StudetFee.objects.get(FeeId=id)
        data.FeeAmount=amount
        data.IssueDate=datetime.now()
        data.save()
        messages.success(request,"Record has been Update")
        return redirect('/finance/fees') 
#  query data
class queryData(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        return redirect('/finance/fees')
    def post(self, request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        year=request.POST['year']
        month=request.POST['month']
       
        data=StudetFee.objects.filter(IssueDate__year=year,IssueDate__month=month)
        dataSet={
            'data':data
        }
        return render(request,'finance/fees.html',dataSet)
        
class CheckTeacher(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')
       
        try:
            id=request.GET['id']
            data=Instructor.objects.filter(Q(tid=id)|Q(username=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
            checkdata=TeacherSalary.objects.filter(Salaryteacher=id)
            currentdate= datetime.now()
            dbdate=checkdata[0].IssueDate
            print("dbmonth",dbdate.month)
            print("db year",dbdate.year)
            print("current month",currentdate.month)
            print("current year",currentdate.year)
            if dbdate.month == currentdate.month:
                return HttpResponse("paid")
            else:
                data=Instructor.objects.filter(Q(tid=id)|Q(username=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
                serdata=SerTeacher(data, many=False)
                return HttpResponse(json.dumps(serdata.data))
            
        except:
            try:
                print("meine")
                id=request.GET['id']
                print(id)
                data=Instructor.objects.get(Q(tid=id)|Q(username=id),uniId=request.session['financeuni'],branchId=request.session['financebranch'])
               
                serdata=SerTeacher(data, many=False)
                return HttpResponse(json.dumps(serdata.data))
            except Exception:
                return HttpResponse("not")
class TeacerSalaryUpdate(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        id= request.GET['id']
        data=TeacherSalary.objects.get(SalaryId=id,uniId=request.session['financeuni'],branchId=request.session['financebranch'])
        print(request.session['financebranch'])
        serdata=serSalary(data, many=False)
        return HttpResponse(json.dumps(serdata.data))
    
    def post(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        id=request.POST['sid']
        amount=request.POST['fee']
        data=TeacherSalary.objects.get(SalaryId=id)
        data.Salaryamount=amount
        data.IssueDate=datetime.now()
        data.save()
        messages.success(request,"Record has been Update")
        return redirect('/finance/salary')

        # Salary Record Delete

class TeacherSalaryDelete(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        id=request.GET.get('id')
        data= TeacherSalary.objects.get(SalaryId=id,uniId=request.session['financeuni'],branchId=request.session['financebranch'])
        print(request.session['financebranch'])
        data.delete()
        messages.error(request,"Record has been Deleted")
        return redirect('/finance/salary')


class queryDataSalary(View):
    def get(self,request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        return redirect('/finance/salary')
    def post(self, request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')


        year=request.POST['year']
        month=request.POST['month']
       
        data=TeacherSalary.objects.filter(IssueDate__year=year,IssueDate__month=month)
        dataSet={
            'data':data
        }
        return render(request,'finance/salary.html',dataSet)
        






# logout all

class LogoutClass(View):
    def get(self, request):
        if request.session.has_key('financeid'):
             del request.session['financeid']
             return redirect('/')
        if request.session.has_key('universitybranchid'):
             del request.session['universitybranchid']
             return redirect('/')
            
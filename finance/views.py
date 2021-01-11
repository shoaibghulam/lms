from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.contrib import messages
from UniversityApp.models import UniversityAccount,UniversityBranch
from .models import  FianceUser,StudetFee
from student.models import Student_Profile,SerStudent
from django.db.models import Q
import json
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
          
      
            
        return render(request,'finance/home.html')
        # return HttpResponse("working")

class TeacherSalary(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')
        return render(request,'finance/salary.html')
        # return HttpResponse("working")


class StudentFees(View):
    def get(self , request):
        if  not(request.session.has_key('financeid') or request.session.has_key('universitybranchid')):
            return redirect('/')

        return render(request,'finance/fees.html')
    def post(self, request):
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
        id=request.GET['id']
        data=Student_Profile.objects.get(Q(StudentId=id)|Q(User_id=id))
        serdata=SerStudent(data, many=False)
        return HttpResponse(json.dumps(serdata.data))

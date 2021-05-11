from django.shortcuts import render , HttpResponse,redirect,HttpResponseRedirect , reverse
from UniversityApp.models import *
from passlib.hash import pbkdf2_sha256
from student.models import *
from administrator.models import *
from faculty.models import *
from library.models import *
from django.contrib import messages
from django.db.models import Case, When
from lmsapp.models import *
from datetime import datetime
from django.db.models import Q
from student.models import *
import json
from urllib.request import urlopen
import pandas as pd
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.mail import send_mail,EmailMultiAlternatives


# Create your views here.
# session login checker
def loginstatus(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
# faculty

def login(request):
    try:
        if request.method=="POST":
            email=request.POST['email']
            password=request.POST['password']

            data=UniversityBranch.objects.get(BranchEmail=email)
            if data:
                if data.UniversityId.UniStatus=="Active":
                    if data.BranchPassword==password:
                        request.session['financeuni']=str(data.UniversityId.UniId)
                        request.session['financebranch']=data.BranchId
                        request.session['universitybranchid']=data.BranchId
                        request.session['universitybranchname']=data.BranchName
                        request.session['universityuniid']=str(data.UniversityId.UniId)
                        return redirect('/university/')
                    else:
                        messages.add_message(request, messages.INFO,
                                         'Please Enter Correct Password')
                        return redirect('/university/login')
                else:
                    return redirect('/university/login')


        return render(request,'uniadmin/adminlogin.html')

    except:
        messages.add_message(request, messages.INFO,
                                         'Please Enter Correct Password')
        return redirect('/university/login')

def logout(request):
    del request.session['universitybranchid']
    del request.session['universityuniid']
    del request.session['universitybranchname']
    return redirect('/university/login')


def index(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    
    Student = Student_Signup.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).count()
    Teacher = User_Signup.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).count()
    return render(request,'uniadmin/home.html',{'studentscount':Student,'facultycount':Teacher})
    # return render(request,'uniadmin/home.html')
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     Student = Student_Signup.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).count()
    #     Teacher = User_Signup.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).count()
    #     return render(request,'uniadmin/home.html',{'studentscount':Student,'facultycount':Teacher})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def branch(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/branch.html')

def profile(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        data=UniversityBranch.objects.filter(UniversityId=request.session['universityuniid'],BranchId=request.session['universitybranchid']).update(BranchUsername=request.POST['BranchUsername'],BranchAddress=request.POST['BranchAddress'],BranchPassword=request.POST['BranchPassword'])
        return HttpResponse("Successfully Updated")
        
    
    data=UniversityBranch.objects.filter(UniversityId=request.session['universityuniid'],BranchId=request.session['universitybranchid'])
    return render(request,'uniadmin/profile.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=UniversityBranch.objects.filter(UniversityId=request.session['uniid'],BranchId=request.session['branchid'])
    #     return render(request,'uniadmin/profile.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    

def faculty(request):
  
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/faculty.html')
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     return render(request,'uniadmin/faculty.html')
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

    
#show contact 
def contact(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Contact.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/admincontact.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Contact.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/admincontact.html',{'data':data})
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
#show contact message
def contactshow(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    
    userdata=list()
    id=request.GET['uid']
    data=Contact.objects.filter(id=id)
    for x in data:
        datas=SerContact(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))

#Delete Contact

def deleteContact(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Contact.objects.get(id=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/contact')


   


#show assignment

def assignment(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    
    if request.method=="POST":
        instructor=request.POST['email']
        data=AssigmentModel.objects.filter(AssigmentTitle__icontains=instructor,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-AsssigmentId')[:]
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        
        return render(request,'uniadmin/adminassignmentmodel.html',{'data':data,'course':course})


    data=AssigmentModel.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-AsssigmentId')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminassignmentmodel.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=AssigmentModel.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminassignmentmodel.html',{'data':data,'course':course})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

    
#Delete Assignment

def deleteassignmemt(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=AssigmentModel.objects.get(AsssigmentId=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/assignment')

def addassignment(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/adminaddassignmentmodel.html')

#show course video

def admincoursevideo(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        ids=list()
        search=request.POST['searchdata']
        instractordata=Instructor.objects.filter(Q(First_Name__icontains=search)|Q(Last_Name__icontains=search))
        for getid in instractordata:
            ids.append(getid.tid)
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        data=CourseVideos.objects.filter(Q(VideoTitle__icontains=search)|Q(InstructerId__in=ids),uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-VideoId')[:]
        return render(request,'uniadmin/admincoursevideo.html',{'data':data,'course':course})
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    data=CourseVideos.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-VideoId')[:]
    return render(request,'uniadmin/admincoursevideo.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     data=CourseVideos.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/admincoursevideo.html',{'data':data,'course':course})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
    
    
    

#Delete course video

def deletecoursevideo(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=CourseVideos.objects.get(VideoId=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/admincoursevideo')


#show depart

def admindepartment(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Did')[:]
    return render(request,'uniadmin/admindepartment.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Department.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-Did')[:]
    #     return render(request,'uniadmin/admindepartment.html',{'data':data})
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')



#ADD DEPARTMENT
def adminadddepartmentf(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            department=request.POST['department']
            desc=request.POST['desc']
            instructor=request.POST['instructor']
        
        
            data=Department(Department_name=department,Dep_Description=desc,Instructor_id=Instructor.objects.get(tid=instructor),uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
            data.save()
            messages.success(request,"Sucessfully Added")
            return redirect('/university/admindepartment')
        teacherlist=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminadddepartmentf.html',{'teacherlist':teacherlist})

    except:
        return redirect('/university/')

# Delete  Department

def deletedepart(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Department.objects.get(Did=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/admindepartment')

#Edit Depart

def editdepart(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            department=request.POST['department']
            desc=request.POST['desc']
            instructor=request.POST['instructor']
            data=Department.objects.get(Did=id)
            data.Department_name=department
            data.Dep_Description=desc
            data.Instructor_id=Instructor.objects.get(tid=instructor)
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/admindepartment')



        depart=Department.objects.get(Did=id)
        tid=depart.Instructor_id.tid
        teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/editdepar.html',{'teacherlist':teacherlist,'depart':depart})
    
    except:
        return redirect('/university/')
    

 #show student result   
def adminexamresult(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')

    if request.method=="POST":
        instructor=request.POST.get('FacultyEmail',False)
        studentemail=request.POST.get('StudentEmail',False)
        if instructor and studentemail:
            instructorid = User_Signup.objects.get(email=instructor)
            instructorProfile = Instructor.objects.get(username = instructorid.user_id)
            getEmail = Student_Signup.objects.get(email=studentemail)
            studentProfile = Student_Profile.objects.get(User_id=getEmail.user_id)
            data=Exam_Result.objects.filter(Student_ID=studentProfile.StudentId,InstructerId=instructorProfile.tid,uniId=request.session['uniiduniversity'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminexamresult.html',{'data':data})

            
        
        if instructor:
            ids=list()
            idslist=list()
            instructorid = User_Signup.objects.filter(Q(email__icontains=instructor)|Q(username__icontains=instructor))
            for getid in instructorid:
                ids.append(getid.user_id)

            instructorProfile = Instructor.objects.filter(username__in =ids)
            for instructorIds in instructorProfile:
                idslist.append(instructorIds.tid)
            data=Exam_Result.objects.filter(InstructerId__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminexamresult.html',{'data':data})
        
        
        if studentemail:
            studentid=list()
            studentlist=list()

            getEmail = Student_Signup.objects.filter(Q(email__icontains=studentemail)|Q(username__icontains=studentemail))
            for getids in getEmail:
                studentid.append(getids.user_id)

            
            studentProfile = Student_Profile.objects.filter(User_id__in=studentid)
            for idlist in studentProfile:
                studentlist.append(idlist.StudentId)
            data=Exam_Result.objects.filter(Student_ID__in=studentlist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminexamresult.html',{'data':data})
       

       
        
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    data=Exam_Result.objects.filter(Status="lock",uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Exam_Result_id')[:]
    return render(request,'uniadmin/adminexamresult.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     data=Exam_Result.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-Exam_Result_id')[:]
    #     return render(request,'uniadmin/adminexamresult.html',{'data':data,'course':course})


    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#show Student emnail suggestion in  Exam:

def ExamEmailSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Student_Signup.objects.filter(email__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.user_id 
            project_json['value'] = project.email
            project_json['label'] = project.email
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


#Update student Result:
def admineditexamresult(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            Gpa=request.POST['gpa']
            projectMarks=request.POST['Pmarks']
            MidMarks=request.POST['Mmarks']
            TotalMarks=request.POST['Tmarks']
            AssignmentMarks=request.POST['Amarks']
            FinalMarks=request.POST['Fmarks']
            result=Exam_Result.objects.get(Exam_Result_id=id)
            result.GPA=Gpa
            result.Project_Marks=projectMarks
            result.Quiz_Assignment_Marks=AssignmentMarks
            result.Midterm_Marks=MidMarks
            result.Final_Marks=FinalMarks
            result.Total_Marks=TotalMarks
            result.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/adminexamresult')
        result=Exam_Result.objects.get(Exam_Result_id=id)
        return render(request,'uniadmin/admineditexamresult.html',{'result':result})

    except:
        return redirect('/university/')

#Delete Student Result

def deletestudentresult(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        data=Exam_Result.objects.get(Exam_Result_id=id)
        data.delete()
        messages.error(request,"Delete Successfully")
        return redirect('/university/adminexamresult')
   
    except:
        return redirect('/university/')


#Faculty Development
def adminfacultydevelopment(request):

    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        
        if request.method == "POST":
            ids=list()
            idslist=list()
            instructor=request.POST['email']
            instructorid = User_Signup.objects.filter(Q(email__icontains=instructor)|Q(username__icontains=instructor))
            for getids in instructorid:
                ids.append(getids.user_id)
            
            instructorProfile = Instructor.objects.filter(username__in = ids)
            for idlist in instructorProfile:
                idslist.append(idlist.tid)

            course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            data=Faculty_Development.objects.filter(Instructor_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminfacultydevelopment.html',{'data':data,'course':course})
    
    except:
        messages.error(request,"Make sure you type correct Email???")
        return redirect('/university/adminfacultydevelopment')

    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    data=Faculty_Development.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Faculty_Development_ID')[:]
    return render(request,'uniadmin/adminfacultydevelopment.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     data=Faculty_Development.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-Faculty_Development_ID')[:]
    #     return render(request,'uniadmin/adminfacultydevelopment.html',{'data':data,'course':course})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

#Delete faculty Development

def deletefacultydevelopment(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Faculty_Development.objects.get(Faculty_Development_ID=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/adminfacultydevelopment')


#show faculty evalution Report
def adminfacultyeval(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        instructor=request.POST['email']
        instructorid = User_Signup.objects.get(email=instructor)
        instructorProfile = Instructor.objects.get(username = instructorid.user_id)
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        data=Faculty_Evaluation.objects.filter(InstructerId=instructorProfile.tid,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminfacultyeval.html',{'data':data,'course':course})
    data=Faculty_Evaluation.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Faculty_Evaluation_ID')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminfacultyeval.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Faculty_Evaluation.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-Faculty_Evaluation_ID')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminfacultyeval.html',{'data':data,'course':course})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#Add Faculty Evalution Report
def adminaddfacultyeval(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            report=request.FILES['reportfile']
            reportname=request.POST['report']
            department=request.POST['depart']
            course=request.POST['course']
            teacher=request.POST['teacher']
            did=Department.objects.get(Did=department)
            cid=Course.objects.get(Cid=course)
            tid=Instructor.objects.get(tid=teacher)
            data=Faculty_Evaluation(Report_Name=reportname,Report_File=reportname,Department_id=did,Course_id=cid,InstructerId=tid,uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('/university/adminfacultyeval')
            
            


        teacher=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminaddfacultyeval.html',{'teacher':teacher,'department':department,'course':course})
    
    except:
        return redirect('/university/')

#Delete Faculty Evalution

def deleteFacultyEvalution(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Faculty_Evaluation.objects.get(Faculty_Evaluation_ID=id)
    data.delete()
    messages.error(request,"Delete Successfully")

    return redirect('/university/adminfacultyeval')

#Edit Faculty Evalution

def admineditfacultyeval(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        if len(request.FILES) != 0:
            reportname=request.POST['reportname']
            reportfile=request.FILES['reportfile']
            depart=request.POST['depart']
            course=request.POST['course']
            teacher=request.POST['teacher']
            did=Department.objects.get(Did=depart)
            cid=Course.objects.get(Cid=course)
            tid=Instructor.objects.get(tid=teacher)
            faculty=Faculty_Evaluation.objects.get(Faculty_Evaluation_ID=id)
            faculty.Report_Name=reportname
            faculty.Report_File=reportfile
            faculty.Department_id=did
            faculty.Course_id=cid
            faculty.InstructerId=tid
            faculty.save()
            messages.success(request,"Updated Successfully")
            return redirect('/university/adminfacultyeval')
        else:
            reportname=request.POST['reportname']
            depart=request.POST['depart']
            course=request.POST['course']
            teacher=request.POST['teacher']
            did=Department.objects.get(Did=depart)
            cid=Course.objects.get(Cid=course)
            tid=Instructor.objects.get(tid=teacher)
            faculty=Faculty_Evaluation.objects.get(Faculty_Evaluation_ID=id)
            faculty.Report_Name=reportname
            faculty.Department_id=did
            faculty.Course_id=cid
            faculty.InstructerId=tid
            faculty.save()
            messages.success(request,"Updated Successfully")
            return redirect('/university/adminfacultyeval')


        
        
    faculty=Faculty_Evaluation.objects.get(Faculty_Evaluation_ID=id)
    tid=faculty.InstructerId.tid
    did=faculty.Department_id.Did
    cid=faculty.Course_id.Cid
    teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    courselist=Course.objects.order_by(Case(When(Cid=cid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    return render(request,'uniadmin/admineditfacultyeval.html',{'teacherlist':teacherlist,'departlist':departlist,'courselist':courselist,'faculty':faculty})




#show Instructor

def admininstructor(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        ids=list()
        instructor=request.POST['instructor']
        dataset=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))
        for idslist in dataset:
            ids.append(idslist.user_id)

        data=Instructor.objects.filter(username__in=ids)
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/admininstructor.html',{'data':data,'course':course})
       
    data=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-tid')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/admininstructor.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Instructor.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-tid')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/admininstructor.html',{'data':data,'course':course})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
    


# Delete Instructor

def deleteinstructor(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Instructor.objects.get(tid=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/admininstructor')

#ADD

def adminaddinstructor(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/adminaddinstructor.html')

#show material class
def adminmaterialclass(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            ids=list()
            idslist=list()
            instructor=request.POST['email']
            instructorid = User_Signup.objects.filter(Q(email__icontains=instructor)|Q(username__icontains=instructor))
            for getids in instructorid:
                ids.append(getids.user_id)
            
            instructorProfile = Instructor.objects.filter(username__in = ids)
            for idlist in instructorProfile:
                idslist.append(idlist.tid)
            data=Materialclass.objects.filter(Instructor_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminmaterialclass.html',{'data':data,'course':course})
    except:
        messages.error(request,"Make Sure You Type Correct Email")
        return redirect('/university/adminmaterialclass')


    result = urlopen('http://just-the-time.appspot.com/')
    result = result.read().strip()
    result_str = result.decode('utf-8')
    present=result_str[:10]
    present = pd.to_datetime(present).date()
  
    data=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
    past=data.UniversityId.UniPackage.PackDurationEnd
    unidata=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
 
    if past >= present and unidata.UniStatus == "Active":
        data=Materialclass.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Materailid')[:]
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminmaterialclass.html',{'data':data,'course':course})
    
    else:
        data=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        data.UniStatus="Disable"
        data.save()
        return redirect('/university/login')
    
#Delete Material class

def deletematerial(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Materialclass.objects.get(Materailid=id)
    data.delete()
    messages.error(request,"Delete Successfully")
    return redirect('/university/adminmaterialclass')

#show notification

def adminnotificationmodel(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method == "POST":
        ids=list()
        idslist=list()
        instructor=request.POST['instructor']
        userdata=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))
        for getid in userdata:
            ids.append(getid.user_id)
        instructorData=Instructor.objects.filter(username__in=ids)
        for getlist in instructorData:
            idslist.append(getlist.tid)
        data=NotificationModel.objects.filter(Instructor_id__in=idslist)
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminnotificationmodel.html',{'data':data,'course':course})
    data=NotificationModel.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-NotificationId')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminnotificationmodel.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=NotificationModel.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-NotificationId')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminnotificationmodel.html',{'data':data,'course':course})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')  

#Delete Notification

def deletenotification(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=NotificationModel.objects.get(NotificationId=id)
    data.delete()
    messages.error(request,"Delete Successfully")
    return redirect('/university/adminnotificationmodel')

#show Quiz

def adminonlinequiz(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method == "POST":
            instructor=request.POST['email']
            ids=list()
            idslist=list()
           
            userdata=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))

            for getid in userdata:
                ids.append(getid.user_id)
            instructorData=Instructor.objects.filter(username__in=ids)

            for getlist in instructorData:
                 idslist.append(getlist.tid)

           
            data=onlinequiz.objects.filter(Instructor_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminonlinequiz.html',{'data':data,'course':course})
    except:
        messages.error(request,"Make Sure You Type Correct Email")
        return redirect('/university/adminonlinequiz')

    data=onlinequiz.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-onlinequizid')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminonlinequiz.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=onlinequiz.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-onlinequizid')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminonlinequiz.html',{'data':data,'course':course})
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#Delete Quiz

def deletequiz(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=onlinequiz.objects.get(onlinequizid=id)
    data.delete()
    messages.error(request,"Delete Successfully")
    return redirect('/university/adminonlinequiz')
    
#show adminquery

def adminqueryadmin(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method == "POST":
        instructor=request.POST['email']
        ids=list()
        idslist=list()
      
        userdata=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))
        for getid in userdata:
            ids.append(getid.user_id)
        instructorData=Instructor.objects.filter(username__in=ids)
        for getlist in instructorData:
            idslist.append(getlist.tid)
        data=Query_Admin.objects.filter(Instructor_id__in=idslist)
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminqueryadmin.html',{'data':data,'course':course})
    data=Query_Admin.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-queryid')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminqueryadmin.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Query_Admin.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-queryid')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminqueryadmin.html',{'data':data,'course':course})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#Edit Admin Query

def admineditqueryadmin(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        
        Rmessage=request.POST['rmessage']
        Querydata=Query_Admin.objects.get(queryid=id)
        Querydata.querystatus=Rmessage
        Querydata.save()
        messages.success(request,"Update Successfully")
        return redirect('/university/adminqueryadmin')

        
        
    data=Query_Admin.objects.get(queryid=id)
    return render(request,'uniadmin/admineditqueryadmin.html',{'data':data})

#Delete Admin query

def deletequery(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Query_Admin.objects.get(queryid=id)
    data.delete()
    messages.error(request,"Delete Successfully")
    return redirect('/university/adminqueryadmin')
    


#show semester

def adminsemes(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-SamesterId')[:]
    return render(request,'uniadmin/adminsemes.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Semester.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-SamesterId')[:]
    #     return render(request,'uniadmin/adminsemes.html',{'data':data})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

#Add Semester

def adminaddsemes(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
   
    if request.method=="POST":
        sname=request.POST['sname']
        scode=request.POST['scode']
        syear=request.POST['syear']
        data=Semester(Samester_Name=sname,Samester_Code=scode,Samester_Year=syear,uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
        data.save()
        messages.success(request,"Added Sucessfully")
        return redirect('/university/adminsemes')
    return render(request,'uniadmin/adminaddsemes.html')

# Delete Semester

def deletesem(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Semester.objects.get(SamesterId=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/adminsemes')

#ADD Course

def adminaddcoursef(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        
        if request.method=="POST":
            coursename=request.POST['cname']
            descriptiom=request.POST['cdesc']
            code=request.POST['ccode']
            totalmarks=request.POST['tmarks']
            obtainmarks=request.POST['omarks']
            midmarks=request.POST['mmarks']
            department=request.POST['department']
            teacher=request.POST['instructor']
            semester=request.POST['semester']
            
            teacherdata=Instructor.objects.get(tid=teacher)
            semesterdata=Semester.objects.get(SamesterId=semester)
            departdata=Department.objects.get(Did=department)
            data=Course(Course_name=coursename,Course_Description=descriptiom,Course_code=code,Total_Marks=totalmarks,Obtain_Marks=obtainmarks,MidTerm_Marks=midmarks,Department_id=departdata,Instructor_id=teacherdata,Semester_id=semesterdata,uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
            data.save()
            messages.success(request,"Added Sucessfully")
            return redirect('/university/admincoursef')

        semester=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        teacher=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminaddcoursef.html',{'semester':semester,'teacher':teacher,'department':department})

    except:
        return redirect('/university/')

#show course 

def admincoursef(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        instructor=request.POST['email']
        instructorid = User_Signup.objects.get(email=instructor)
        instructorProfile = Instructor.objects.get(username = instructorid.user_id)
        data=Course.objects.filter(Instructor_id=instructorProfile.tid,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/admincoursef.html',{'data':data,'course':course})
    
    data=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Cid')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/admincoursef.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-Cid')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/admincoursef.html',{'data':data,'course':course})


    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
    

# Delete course

def deletecourse(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Course.objects.get(Cid=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/admincoursef')

#Edit course

def Editcourse(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        coursename=request.POST['cname']
        descriptiom=request.POST['cdesc']
        code=request.POST['ccode']
        totalmarks=request.POST['tmarks']
        obtainmarks=request.POST['omarks']
        midmarks=request.POST['mmarks']
        department=request.POST['department']
        teacher=request.POST['instructor']
        semester=request.POST['semester']

        courseData=Course.objects.get(Cid=id)
        courseData.Course_name=coursename
        courseData.Course_Description=descriptiom
        courseData.Course_code=code
        courseData.Total_Marks=totalmarks
        courseData.Obtain_Marks=obtainmarks
        courseData.MidTerm_Marks=midmarks
        courseData.Course_code=code

        teacherdata=Instructor.objects.get(tid=teacher)
        semesterdata=Semester.objects.get(SamesterId=semester)
        departdata=Department.objects.get(Did=department)

        courseData.Department_id=departdata
        courseData.Instructor_id=teacherdata
        courseData.Semester_id=semesterdata
        courseData.save()

        messages.success(request,"Update Sucessfully")
        return redirect('/university/admincoursef')


    courseData=Course.objects.get(Cid=id)
    did=courseData.Department_id.Did
    tid=courseData.Instructor_id.tid
    sid=courseData.Semester_id.SamesterId
    teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    semesterlist=Semester.objects.order_by(Case(When(SamesterId=sid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    return render(request,'uniadmin/editcourse.html',{'department':departlist,'teacher':teacherlist,'semester':semesterlist,'course':courseData})


#show Teacher application

def adminteacherapplication(request):

    
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method == "POST":
        instructor=request.POST['email']
        ids=list()
        idslist=list()
      
        userdata=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))
        for getid in userdata:
            ids.append(getid.user_id)
        instructorData=Instructor.objects.filter(username__in=ids)
        for getlist in instructorData:
            idslist.append(getlist.tid)

        data=TeacherApplication.objects.filter(Instructor_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-ApplicationId')[:]
        course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminteacherapplication.html',{'data':data,'course':course})


    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    data=TeacherApplication.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-ApplicationId')[:]
    return render(request,'uniadmin/adminteacherapplication.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     data=TeacherApplication.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-ApplicationId')[:]
    #     return render(request,'uniadmin/adminteacherapplication.html',{'data':data,'course':course})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
    
# Delete teacher application

def deleteapplication(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=TeacherApplication.objects.get(ApplicationId=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/adminteacherapplication')

#edit teacher application

def editteacherapplication(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        replymessage=request.POST['rmessage']
        data=TeacherApplication.objects.get(ApplicationId=id)
        data.ApplicationStatus=replymessage
        data.save()
        messages.success(request,"Updated Sucessfully")
        return redirect('/university/adminteacherapplication')

    data=TeacherApplication.objects.get(ApplicationId=id)
    return render(request,'uniadmin/editapplication.html',{'data':data})



#Add
def adminaddteacherapp(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/adminaddteacherapp.html')


# show teacher syllabus

def adminteachersyllabus(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=='POST':
            instructor=request.POST['email']
            ids=list()
            idslist=list()
      
            userdata=User_Signup.objects.filter(Q(username__icontains=instructor)|Q(email__icontains=instructor))
            for getid in userdata:
                ids.append(getid.user_id)
            instructorData=Instructor.objects.filter(username__in=ids)
            for getlist in instructorData:
                idslist.append(getlist.tid)
            
           
            data=Teacher_syllabus.objects.filter(Instructor_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminteachersyllabus.html',{'data':data,'course':course})
        

    except:
        messages.error(request,"Make Sure You Type Correct Email????")
        return redirect('/university/adminteachersyllabus')

    data=Teacher_syllabus.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-syllabusId')[:]
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminteachersyllabus.html',{'data':data,'course':course})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Teacher_syllabus.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-syllabusId')[:]
    #     course=Course.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminteachersyllabus.html',{'data':data,'course':course})

    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
 
#ADD Teacher syllabus

def adminaddteachsyllabus(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        semester=request.POST['semester']
        syllabusFile=request.FILES['file']
        course=request.POST['course']
        depart=request.POST['department']
        teacher=request.POST['teacher']
        courseid=Course.objects.get(Cid=course)
        departid=Department.objects.get(Did=depart)
        teacherid=Instructor.objects.get(tid=teacher)
        data=Teacher_syllabus(semester=semester,outline=syllabusFile,Course_id=courseid,Instructor_id=teacherid,Department_id=departid,uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
        data.save()
        messages.success(request,"Added Sucessfully")
        return redirect('/university/adminteachersyllabus')
    


    semester=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    teacher=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddteachsyllabus.html',{'semester':semester,'department':department,'teacher':teacher,'course':course})

#Delete Teacher Syllabus

def deleteteachersyllabus(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=Teacher_syllabus.objects.filter(syllabusId=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/adminteachersyllabus')


#Update Teacher Syllabus

def Editsyllabus(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method=="POST":
        
        if len(request.FILES)!=0:
            semester=request.POST['semester']
            semesterFile=request.FILES['file']
            course=Course.objects.get(Cid=request.POST['course'])
            teacher=Instructor.objects.get(tid=request.POST['teacher'])
            depart=Department.objects.get(Did=request.POST['department'])
            syllabus=Teacher_syllabus.objects.get(syllabusId=id)
            syllabus.semester=semester
            syllabus.Course_id=course
            syllabus.Instructor_id=teacher
            syllabus.Department_id=depart
            syllabus.outline=semesterFile
            syllabus.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/university/adminteachersyllabus')
        else:
            semester=request.POST['semester']
            course=Course.objects.get(Cid=request.POST['course'])
            teacher=Instructor.objects.get(tid=request.POST['teacher'])
            depart=Department.objects.get(Did=request.POST['department'])
            syllabus=Teacher_syllabus.objects.get(syllabusId=id)
            syllabus.semester=semester
            syllabus.Course_id=course
            syllabus.Instructor_id=teacher
            syllabus.Department_id=depart
            syllabus.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/university/adminteachersyllabus')

        
        
    syllabus=Teacher_syllabus.objects.get(syllabusId=id)
    tid=syllabus.Instructor_id.tid
    did=syllabus.Department_id.Did
    cid=syllabus.Course_id.Cid
    semesterName=syllabus.semester
    semesterlist=Semester.objects.order_by(Case(When(Samester_Name=semesterName,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    courselist=Course.objects.order_by(Case(When(Cid=cid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
    return render(request,"uniadmin/Editsyllabus.html",{'semester':semesterlist,'course':courselist,'teacher':teacherlist,'department':departlist,'syllabus':syllabus})

#show signup table

def adminusersignup(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.method == "POST":
        email=request.POST['email']
        data=User_Signup.objects.filter(Q(email__icontains=email)|Q(username__icontains=email),uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminusersignup.html',{'data':data})

    data=User_Signup.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-user_id')[:]
    return render(request,'uniadmin/adminusersignup.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=User_Signup.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-user_id')[:]
    #     return render(request,'uniadmin/adminusersignup.html',{'data':data})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

#signup Suggestion
def signupSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = User_Signup.objects.filter(email__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.user_id 
            project_json['value'] = project.email
            project_json['label'] = project.email
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

   

#Delete Signup table

def deletesignup(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        data=User_Signup.objects.filter(user_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminusersignup')
    except:
        return redirect('/university/')

#Edit Signup

def editsignup(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            # email=request.POST['email']
            # checkrepeat=User_Signup.objects.filter(email=email)
            # if checkrepeat:
            #     messages.error(request,"Email ALready Exist")
            #     return redirect('adminaddusersign')
            email=request.POST['email']
            username=request.POST['username']
            password=request.POST['password']
            data=User_Signup.objects.get(user_id=id)
            data.username=username
            data.email=email
            data.password=password
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/adminusersignup')
            
        
            
        data=User_Signup.objects.filter(user_id=id)
        return render(request,'uniadmin/editsignup.html',{'data':data})
    except:
        return redirect('/university/')

    


#Add USER SIGNUP ACCOUNT

def adminaddusersign(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            package = uniid.UniPackage.PackTeacher 
            userCount = User_Signup.objects.filter(uniId=request.session['universityuniid']).count()
            if package<=userCount:
                messages.error(request,"Your Faculty Limit  is "+str(package)+" and Your Limit is Full Please Contact the Admin")
                return redirect('adminaddusersign')

            email=request.POST['email']
            checkrepeat=User_Signup.objects.filter(email=email)
            if checkrepeat:
                messages.error(request,"Email ALready Exist")
                return redirect('adminaddusersign')
            password=request.POST['password']
            username=request.POST['username']
            role=request.POST['role']
            verify=request.POST['verify']
            data=User_Signup(username=username,email=email,password=password,verify=verify,role=role,uniId=uniid,branchId=branchid)
            data.save()
            user=User_Signup.objects.get(user_id=data.pk)
            firstname=request.POST['fname']
            lastname=request.POST['lname']
            gender=request.POST['gender']
            contact=request.POST['contact']
            address=request.POST['address']
            dob=request.POST['dob']
            image=request.FILES['image']
            profilesave=Instructor(First_Name=firstname,Last_Name=lastname,Gender=gender,Address=address,Phone_Number=contact,Dob=dob,img=image,username=user,uniId=uniid,branchId=branchid)
            
          
            profilesave.save()

            messages.success(request,"Save Successfully")
            facultycredentials(request,data.pk)
            return redirect('adminusersignup')
          
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminaddusersign.html')


#show faculty userstories

def adminuserstory(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=User_Stories.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-storyid')[:]
    return render(request,'uniadmin/adminuserstory.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=User_Stories.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid']).order_by('-storyid')[:]
    #     return render(request,'uniadmin/adminuserstory.html',{'data':data})
    
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


  

#Delete Facultyuser stories

def deleteFacultyUserStories(request,id):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    data=User_Stories.objects.filter(storyid=id)
    data.delete()
    messages.error(request,"Delete Sucessfully")
    return redirect('/university/adminuserstory')


#student shakeeb work

def admineditquery(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    return render(request,'uniadmin/admineditquery.html')



















































































































































































































































































































































































































































































































































































































#student

def student(request):

    return render(request,'uniadmin/student.html')
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     return render(request,'uniadmin/student.html')
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def adminapplication(request):
    if request.method == "POST":
        ids =list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=Application.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminapplication.html',{'data':data})
    data=Application.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-ApplicationId')[:]
    return render(request,'uniadmin/adminapplication.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Application.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminapplication.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def Suggestionadminapplication(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def deleteadminapplication(request,id):
    try:
        data=Application.objects.filter(ApplicationId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminapplication')
    except:
        return redirect('/university/')
def adminjob(request):
    try:
        if request.method == "POST":
            ids=list()
            query=request.POST['student']
            student=Student_Profile.objects.filter(Q(First_name__icontains=query)|Q(Last_name__icontains=query))
            for getid in student:
                ids.append(getid.StudentId)
            data=Job_Apply.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminjob.html',{'data':data})
    except:
        redirect('/adminjob')

    
    data=Job_Apply.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Job_Apply_id')[:]
    return render(request,'uniadmin/adminjob.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Job_Apply.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminjob.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def Suggestionadminjob(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def deleteadminjob(request,id):
    try:
        data=Job_Apply.objects.filter(Job_Apply_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminjob')
    except: 
        return redirect('/university/')

def adminmeeting(request):
    try:
        studentids=list()
        if request.method == "POST":
            student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
            for ids in student:
                studentids.append(ids.StudentId)

            data=MeetingAppointment.objects.filter(Student_ID__in=studentids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/adminmeeting.html',{'data':data})
        
        data=MeetingAppointment.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Appointment_id')[:]
        return render(request,'uniadmin/adminmeeting.html',{'data':data})
        # result = urlopen('http://just-the-time.appspot.com/')
        # result = result.read().strip()
        # result_str = result.decode('utf-8')
        # present=result_str[:10]
        # present = pd.to_datetime(present).date()
    
        # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
        # past=data.UniversityId.UniPackage.PackDurationEnd
        # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
    
        # if past >= present and unidata.UniStatus == "Active":
        #     data=MeetingAppointment.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
            # return render(request,'uniadmin/adminmeeting.html',{'data':data})

        # else:
        #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
        #     data.UniStatus="Disable"
        #     data.save()
        #     return redirect('/university/login')
    except:
        return HttpResponse("hello")

def Suggestionadminmeeting(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def deleteadminmeeting(request,id):
    try:
        data=MeetingAppointment.objects.filter(Appointment_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminmeeting')
    except:
        return redirect('/university/')

def adminregister(request):
    if request.method == "POST":
        ids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=Registration.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminregister.html',{'data':data})
    data=Registration.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Student_Registration_Id')[:]
    return render(request,'uniadmin/adminregister.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Registration.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
        # return render(request,'uniadmin/adminregister.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminregister(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def deleteadminregister(request,id):
    try:
        data=Registration.objects.filter(Student_Registration_Id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminregister')
    except:
        return redirect('/university/')

def adminaddregister(request):

    try:
        if request.method=="POST":
            student=Student_Profile.objects.get(StudentId=request.POST['student']) 
            Student_Program=request.POST['Student_Program']
            Student_Registration_Code=request.POST['Student_Registration_Code']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Registration(Student_Program=Student_Program,Student_Registration_Code=Student_Registration_Code,uniId=uniid,branchId=branchid,Student_id=student)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminregister')
        
    except:
        return redirect('/university/')   
    student=Student_Profile.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddregister.html',{'data':student})
    

def editadminaddregister(request,id):
  
   
    try:
        if request.method=="POST":
            
            student=Student_Profile.objects.get(StudentId=request.POST['student']) 
            Student_Program=request.POST['Student_Program']
            Student_Registration_Code=request.POST['Student_Registration_Code']
            
            data=Registration.objects.get(Student_Registration_Id=id)
            data.Student_Program=Student_Program
            data.Student_Registration_Code=Student_Registration_Code
            data.Student_id=student
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/adminregister')

        data=Registration.objects.get(Student_Registration_Id=id)
        sid=data.Student_id.StudentId
        student=Student_Profile.objects.order_by(Case(When(StudentId=sid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/editadminaddregister.html',{'data':data,'student':student})

    except:
        return redirect('/university/')

def adminscruntiy(request):
    idslist=list()
    if request.method == "POST":
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for ids in student:
            idslist.append(ids.StudentId)

        data=ScrunityForm.objects.filter(Student_id__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminscruntiy.html',{'data':data})
    
    data=ScrunityForm.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Scrunity_Form_Id')[:]
    return render(request,'uniadmin/adminscruntiy.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=ScrunityForm.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminscruntiy.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminscruntiy(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminscruntiy(request,id):
    try:
        data=ScrunityForm.objects.filter(Scrunity_Form_Id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminscruntiy')
    except:
        return redirect('/university/')

def adminassignmet(request):
    if request.method == "POST":
        assigmentids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for ids in student:
            assigmentids.append(ids.StudentId)
        
        data=Student_Assigment.objects.filter(Student_id__in=assigmentids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminassignmet.html',{'data':data})
    
    data=Student_Assigment.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Student_Assigment_Id')[:]
    return render(request,'uniadmin/adminassignmet.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Assigment.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminassignmet.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminassignmet(request):
    if not request.session.has_key('branchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminassignmet(request,id):
    try:
        data=Student_Assigment.objects.filter(Student_Assigment_Id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminassignmet')
    except:
        return redirect('/university/')



def adminquery(request):
    if request.method == "POST":
        queryids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for ids in student:
            queryids.append(ids.StudentId)
        data=Student_Query_Admin.objects.filter(Student_ID__in=queryids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminquery.html',{'data':data})
    
    data=Student_Query_Admin.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-queryid')[:]
    return render(request,'uniadmin/adminquery.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Query_Admin.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminquery.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminquery(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminquery(request,id):
    try:
        data=Student_Query_Admin.objects.filter(queryid=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminquery')
    except:
        return redirect('/university/')

def adminstudentevalution(request):
    if request.method == "POST":
        ids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=Student_Submit_Evaluation.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminstudentevalution.html',{'data':data})
    data=Student_Submit_Evaluation.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Student_Submit_Evaluation_id')[:]
    return render(request,'uniadmin/adminstudentevalution.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Query_Admin.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminquery.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminstudentevalution(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
    
def deleteadminstudentevalution(request,id):
    try:
        data=Student_Submit_Evaluation.objects.filter(Student_Submit_Evaluation_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminstudentevalution')
    except:
        return redirect('/university/')



def adminsurveryans(request):
    if request.method == "POST":
        ids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=Student_Survey.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminsurveryans.html',{'data':data})
    
    data=Student_Survey.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Survey_id')[:]
    return render(request,'uniadmin/adminsurveryans.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Survey.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
        # return render(request,'uniadmin/adminsurveryans.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminsurveryans(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminsurveryans(request,id):
    try:
        data=Student_Survey.objects.filter(Survey_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminsurveryans')
    except:
        return redirect('/university/')


#show and search courses
def admincourse(request):
    if request.method == "POST":
        
        department = request.POST['depart']
        semester = request.POST['semester']
        CourseData = Course.objects.filter(Department_id=department,Semester_id=semester)
        depart  = Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        semester = Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        batch = Batch.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/InsertCourse.html',{'depart':depart,'semester':semester,'course':CourseData,'batch':batch})


            
    CourseData = Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    depart  = Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    semester = Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    batch = Batch.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/InsertCourse.html',{'depart':depart,'semester':semester,'course':CourseData,'batch':batch})

#Admin add courses
def AdminAddCourses(request):
    try:
        if request.method == "POST":
            
            department =Department.objects.get(Did=request.POST['depart']) 
            semester =Semester.objects.get(SamesterId=request.POST['semester'])
            batch =Batch.objects.get(Batch_id=request.POST['batch'])
            courselist=request.POST.getlist('courselist','off')
            # if course is unchecked  redirect
            if courselist == "off":
                messages.error(request,"Make Sure Course are Check At least One")
                return redirect('/university/admincourse')
            # if course is unchecked  redirect end
           
            # condtion for those student who already enrolled in course start
            studentsids= list()
            studentdata=Student_Course.objects.filter(Q(Courses__in=courselist),Department_id=department,Semester_ID=semester,StudenBatch=batch)
            for x in studentdata:
                studentsids.append(x.Student_ID.StudentId)
            # condtion for those student who already enrolled in course end

            students=Student_Profile.objects.filter(~Q(StudentId__in=studentsids),StudenBatch=batch,Department_id=department,Semester_ID=semester)
           
          
            if students:
                for st in students:
                    stcourse=Student_Course.objects.create(Student_ID=st,Department_id=department,Semester_ID=semester,StudenBatch=batch,uniId=UniversityAccount.objects.get(UniId=request.session['universityuniid']),branchId=UniversityBranch.objects.get(BranchId=request.session['universitybranchid']))
                    for courseid in courselist:
                        stcourse.Courses.add(Course.objects.get(Cid=courseid))
                    stcourse.save()
            

                        
                messages.success(request,"Courses Added Sucessfully")
                return redirect('/university/admincourse')
            else:
                 messages.success(request,"All Students enrolled in the course")
                 return redirect('/university/admincourse')

    
    except:
        messages.error(request,"Make Sure Course are Check At least One")
        return redirect('/university/admincourse')

    
   #student course show and search
def deleteCourse(request):
    try:
        if request.method == "POST":
            department = request.POST['depart']
            semester = request.POST['semester']
            batch = request.POST['batch']
            request.session['departid']=department
            request.session['semester']=semester
            request.session['batch']=batch
            studentCouse = Student_Course.objects.filter(Department_id=department,Semester_ID=semester,StudenBatch=batch)[0]
            courseidlist = []
            for i in studentCouse.Courses.all():
                courseidlist.append(i.Cid)

            courseData = Course.objects.filter(Cid__in = courseidlist)
            depart  = Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            semester = Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            batch = Batch.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            return render(request,'uniadmin/DeleteCourse.html',{'depart':depart,'semester':semester,'batch':batch,'course':courseData})


        depart  = Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        semester = Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        batch = Batch.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/DeleteCourse.html',{'depart':depart,'semester':semester,'batch':batch})
    
    except:
        return redirect('/university/deleteCourse')


#Delete student course 

def deleteCourseID(request,id):

    request.session['departid']
    request.session['semester']
    request.session['batch']
    studentCourse = Student_Course.objects.filter(Department_id=request.session['departid'],Semester_ID=request.session['semester'],StudenBatch=request.session['batch'])
    for i in studentCourse:
        i.Courses.remove(Course.objects.get(Cid =id))
    
    del request.session['departid']
    del request.session['semester']
    del request.session['batch']   
    
    messages.error(request,"Delete Course Sucessfully")
    return redirect('/university/deleteCourse')
    
        



    
    
   
    

    

def adminsprofile(request):
    
    if request.method == "POST":
        ids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=Student_Profile.objects.filter(StudentId__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminsprofile.html',{'data':data})
    
    data=Student_Profile.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-StudentId')[:]
    return render(request,'uniadmin/adminsprofile.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Profile.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
        # return render(request,'uniadmin/adminsprofile.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggadminsprofile(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminsprofile(request,id):
    try:
        data=Student_Profile.objects.filter(StudentId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminsprofile')
    except:
        return redirect('/university/')

def adminsignup(request):
    
    if request.method == "POST":
        email=request.POST['email']
        data=Student_Signup.objects.filter(Q(email__icontains=email)|Q(username__icontains=email),uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminsignup.html',{'data':data})
    
    data=Student_Signup.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-user_id')[:]
    return render(request,'uniadmin/adminsignup.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Student_Signup.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminsignup.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
def Suggestionadminsignup(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Signup.objects.filter(email__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.user_id 
            project_json['value'] = project.email
            project_json['label'] = project.email
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def deleteadminsignup(request,id):
    try:
        data=Student_Signup.objects.filter(user_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminsignup')
    except:
        return redirect('/university/')



def adminaddsignup(request):
    try:
        if not request.session.has_key('universitybranchid'):
            return redirect('/university/login')
        if request.method=="POST":
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            package = uniid.UniPackage.PackStudent
            userCount = Student_Signup.objects.filter(uniId=request.session['universityuniid']).count()
            if package<=userCount:
                messages.error(request,"Your Student Limit  is "+str(package)+" and Your Limit is Full Please Contact the Admin")
                return redirect('adminaddsignup')
           
            email=request.POST['email']
            checkrepeat=Student_Signup.objects.filter(email=email)
            if checkrepeat:
                messages.error(request,"Email ALready Exist")
                return redirect('adminaddsignup')
            password=request.POST['password']
            username=request.POST['username']
            role=request.POST['role']
            verify=request.POST['verify']
            data=Student_Signup(username=username,email=email,password=password,verify=verify,role=role,uniId=uniid,branchId=branchid)
            data.save()
            firstname=request.POST['fname']
            lastname=request.POST['lname']
            address=request.POST['address']
            contact=request.POST['contact']
            batch=request.POST['batch']
            department=request.POST['department']
            dob=request.POST['dob']
            shift=request.POST['shift']
            sem=request.POST['semester']
            image = request.FILES.get('image',False)
            depart=Department.objects.get(Did=department,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            semesterid=Semester.objects.get(SamesterId=sem,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            userid=Student_Signup.objects.get(pk=data.user_id)
            batchid = Batch.objects.get(Batch_id=batch,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
            profiledata=Student_Profile(First_name=firstname,Last_name=lastname,ContactNo=contact,Address=address,DOB=dob,StudenBatch=batchid,StudenShift=shift,Profile=image,
Department_id=depart,Semester_ID=semesterid,uniId=uniid,branchId=branchid,
User_id=userid)
            profiledata.save()


            messages.success(request,"Save Successfully")
            studentcredentials(request, data.pk)
            return redirect('adminsignup')
            

    except:
        return redirect('/university/')
    batch = Batch.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    semester=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddsignup.html',{'batch':batch,'department':department,'semester':semester})
    

def editadminsignup(request,id):
    try:
        if not request.session.has_key('universitybranchid'):
                return redirect('/university/login')
        if request.method=="POST":
            email=request.POST['email']
            username=request.POST['username']
            password=request.POST['password']
            data=Student_Signup.objects.get(user_id=id)
            data.username=username
            data.email=email
            data.password=password
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/adminsignup')
                
            
                
        data=Student_Signup.objects.filter(user_id=id)
        return render(request,'uniadmin/editadminsignup.html',{'data':data})
        
    except:
        return redirect('/university/')


















































































































    


























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































#library
    

def bookauther(request):

    if request.method == "POST":
        BookAuthorFirstName=request.POST['BookAuthorFirstName']
        data=BookAuthor.objects.filter(BookAuthorFirstName__icontains=BookAuthorFirstName,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminbookauthor.html',{'data':data})

    data=BookAuthor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-BookAuthorId')[:]
    return render(request,'uniadmin/adminbookauthor.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=BookAuthor.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminbookauthor.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
    


def adminaddbookauthor(request):
    try:
        if request.method=="POST":
            BookAuthorFirstName=request.POST['BookAuthorFirstName']
            BookAuthorLastName=request.POST['BookAuthorLastName']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=BookAuthor(BookAuthorFirstName=BookAuthorFirstName,BookAuthorLastName=BookAuthorLastName,uniId=uniid,branchId=branchid)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('bookauther')
        
    except:
        return redirect('/university/')   

    return render(request,'uniadmin/adminaddbookauthor.html')        

#bookauthorSuggestion
def bookauthorSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = BookAuthor.objects.filter(BookAuthorFirstName__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.BookAuthorId 
            project_json['value'] = project.BookAuthorFirstName
            project_json['label'] = project.BookAuthorFirstName
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
def deleteadminaddbookauthor(request,id):
    try:
        data=BookAuthor.objects.filter(BookAuthorId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('bookauther')
    except:
        return redirect('/university/')
def editadminaddbookauthor(request,id):
    try:
        if request.method=="POST":
            BookAuthorLastName=request.POST['BookAuthorFirstName']
            BookAuthorLastName=request.POST['BookAuthorLastName']
            data=BookAuthor.objects.get(BookAuthorId=id)
            data.BookAuthorLastName=BookAuthorLastName
            data.BookAuthorLastName=BookAuthorLastName
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('bookauther')
        data=BookAuthor.objects.filter(BookAuthorId=id)
        return render(request,'uniadmin/editadminaddbookauthor.html',{'data':data})
            
    except:
        return redirect('/university/')

def book(request):
    if request.method == "POST":
        BookTitle=request.POST['BookTitle']
        data=Books.objects.filter(BookTitle__icontains=BookTitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminbook.html',{'data':data})
    data=Books.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-BookId')[:]
    return render(request,'uniadmin/adminbook.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Books.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminbook.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
#bookSuggestion Suggestion
def bookSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Books.objects.filter(BookTitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.BookId 
            project_json['value'] = project.BookTitle
            project_json['label'] = project.BookTitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def adminaddbook(request):

    
    try:
        if request.method=="POST":

            BookTitle=request.POST['BookTitle']
            BookAuthorname=BookAuthor.objects.get(BookAuthorId=request.POST['BookAuthorname']) 
            BookEdition=request.POST['BookEdition']
            BookPublisher=request.POST['BookPublisher']
            BookYearOfPublisher=request.POST['BookYearOfPublisher']
            BookISBN=request.POST['BookISBN']
            Bookcategory=request.POST['Bookcategory']
            BookFile=request.FILES['BookFile']
            BookCoverPage=request.FILES['BookCoverPage']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Books(BookTitle=BookTitle,BookAuthorid=BookAuthorname,BookEdition=BookEdition,BookPublisher=BookPublisher,BookYearOfPublisher=BookYearOfPublisher,BookISBN=BookISBN,Bookcategory=Bookcategory,BookFile=BookFile,BookCoverPage=BookCoverPage,uniId=uniid,branchId=branchid)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('book')
        
        data=BookAuthor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminaddbook.html',{'data':data})
        
    except:
        return redirect('/university/')  
    
def deleteadminaddbook(request,id):
    try:
        data=Books.objects.filter(BookId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('book')
    except:
        return redirect('/university/')

def editadminaddbook(request,id):
  
   
    try:
        if request.method=="POST":
            
            BookTitle=request.POST['BookTitle']
            BookAuthorname=BookAuthor.objects.get(BookAuthorId=request.POST['BookAuthorname']) 
            BookEdition=request.POST['BookEdition']
            BookPublisher=request.POST['BookPublisher']
            BookYearOfPublisher=request.POST['BookYearOfPublisher']
            BookISBN=request.POST['BookISBN']
            Bookcategory=request.POST['Bookcategory']
            data=Books.objects.get(BookId=id)
            data.BookTitle=BookTitle
            data.BookAuthorid=BookAuthorname
            data.BookEdition=BookEdition
            data.BookPublisher=BookPublisher
            data.BookYearOfPublisher=BookYearOfPublisher
            data.BookISBN=BookISBN
            data.Bookcategory=Bookcategory
            BookFile=request.FILES.get('BookFile', False)
            if BookFile:
                data.BookFile=BookFile

            BookCoverPage=request.FILES.get('BookCoverPage',False)
            
            if BookCoverPage:
                data.BookCoverPage=BookCoverPage

            data.save()
            messages.success(request,"Update Successfully")
            return redirect('/university/book')


        bookdata=Books.objects.get(BookId=id)
        bookid=bookdata.BookAuthorid.BookAuthorId
        bookc=bookdata.Bookcategory
        bookcategory=Books.objects.order_by(Case(When(Bookcategory=bookc,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        book=BookAuthor.objects.order_by(Case(When(BookAuthorId=bookid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        data=Books.objects.order_by(Case(When(BookId=id,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/editadminaddbook.html',{'data':bookdata,'book':book,'category':data,'bookcategory':bookcategory})

    except:
        return redirect('/university/')
       








#admin panel

def admindashboard(request):
    return render(request,'uniadmin/admin-dashboard.html')
    
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     return render(request,'uniadmin/admin-dashboard.html')
    # else:
        
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def academiccalendarmodel(request):
    if request.method == "POST":
        AcademicCalendarTitle=request.POST['AcademicCalendarTitle']
        data=AcademicCalendarModel.objects.filter(AcademicCalendarTitle__icontains=AcademicCalendarTitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/academiccalendarmodel.html',{'data':data})
    data=AcademicCalendarModel.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-AcademicCalendarId')[:]
    return render(request,'uniadmin/academiccalendarmodel.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=AcademicCalendarModel.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/academiccalendarmodel.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
    
        
#academiccalendarmodel Suggestion 
def academiccalendarmodelSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = AcademicCalendarModel.objects.filter(AcademicCalendarTitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.AcademicCalendarId 
            project_json['value'] = project.AcademicCalendarTitle
            project_json['label'] = project.AcademicCalendarTitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

    
    
def newcalendarmodel(request):
    try:

        if request.method=="POST":

            AcademicCalendarTitle=request.POST['AcademicCalendarTitle']
            AcademicCalendarDesc=request.POST['AcademicCalendarDesc']
            AcademicCalendarStartDate=request.POST['AcademicCalendarStartDate']
            AcademicCalendarEndDate=request.POST['AcademicCalendarEndDate']
            AcademicCalendarLocation=request.POST['AcademicCalendarLocation']
            Image=request.FILES['Image']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=AcademicCalendarModel(AcademicCalendarTitle=AcademicCalendarTitle,AcademicCalendarDesc=AcademicCalendarDesc,AcademicCalendarStartDate=AcademicCalendarStartDate,AcademicCalendarEndDate=AcademicCalendarEndDate,AcademicCalendarLocation=AcademicCalendarLocation,Image=Image,uniId=uniid,branchId=branchid)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('academiccalendarmodel')

            
    except:
        return redirect('/university/')  

    return render(request,'uniadmin/newcalendarmodel.html')

def deletecalendarmodel(request,id):
    try:
        data=AcademicCalendarModel.objects.filter(AcademicCalendarId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('academiccalendarmodel')
    except:
        return redirect('/university/')


def editcalendarmodel(request,id):
    try:
        if request.method=="POST":
            AcademicCalendarTitle=request.POST['AcademicCalendarTitle']
            AcademicCalendarDesc=request.POST['AcademicCalendarDesc']
            AcademicCalendarStartDate=request.POST['AcademicCalendarStartDate']
            AcademicCalendarEndDate=request.POST['AcademicCalendarEndDate']
            AcademicCalendarLocation=request.POST['AcademicCalendarLocation']
            Image=request.FILES.get('Image',False)
          
            data=AcademicCalendarModel.objects.get(AcademicCalendarId=id)
            data.AcademicCalendarTitle=AcademicCalendarTitle
            data.AcademicCalendarDesc=AcademicCalendarDesc
            data.AcademicCalendarStartDate=AcademicCalendarStartDate
            data.AcademicCalendarEndDate=AcademicCalendarEndDate
            data.AcademicCalendarLocation=AcademicCalendarLocation
            if Image:
                data.Image=request.FILES['Image']
                print("Hello world")
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('academiccalendarmodel')
        data=AcademicCalendarModel.objects.filter(AcademicCalendarId=id)
        return render(request,'uniadmin/editcalendarmodel.html',{'data':data})
            
    except:
        return redirect('/university/')
    



def adminfacultycalendar(request):
    if request.method == "POST":
        FacultyCalendarTitle=request.POST['FacultyCalendarTitle']
        data=FacultyCalendarModel.objects.filter(FacultyCalendarTitle__icontains=FacultyCalendarTitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminfacultycalendar.html',{'data':data})
    data=FacultyCalendarModel.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-FacultyCalendarId')[:]
    return render(request,'uniadmin/adminfacultycalendar.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=FacultyCalendarModel.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminfacultycalendar.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
#adminfacultycalendar Suggestion 
def adminfacultycalendarSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = FacultyCalendarModel.objects.filter(FacultyCalendarTitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.FacultyCalendarId 
            project_json['value'] = project.FacultyCalendarTitle
            project_json['label'] = project.FacultyCalendarTitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
    

def adminaddfacultycalendar(request):
    try:
        if request.method=="POST":


            FacultyCalendarTitle=request.POST['FacultyCalendarTitle']
            FacultyCalendarDesc=request.POST['FacultyCalendarDesc']
            FacultyCalendarStartDate=request.POST['FacultyCalendarStartDate']
            FacultyCalendarEndDate=request.POST['FacultyCalendarEndDate']
            FacultyCalendarLocation=request.POST['FacultyCalendarLocation']
            did=Department.objects.get(Did=request.POST['department']) 
            Image=request.FILES['Image']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=FacultyCalendarModel(FacultyCalendarTitle=FacultyCalendarTitle,FacultyCalendarDesc=FacultyCalendarDesc,FacultyCalendarStartDate=FacultyCalendarStartDate,FacultyCalendarEndDate=FacultyCalendarEndDate,FacultyCalendarLocation=FacultyCalendarLocation,Image=Image,uniId=uniid,branchId=branchid,Department_id=did)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminfacultycalendar')
    

    except:
        return redirect('/university/')

    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddfacultycalendar.html',{'department':department})
    
def deletefacultycalendarmodel(request,id):
    try:
        data=FacultyCalendarModel.objects.filter(FacultyCalendarId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminfacultycalendar')
    except:
        return redirect('/university/')

def admineditfacultycalendar(request,id):
    try:
        if request.method=="POST":
            FacultyCalendarTitle=request.POST['FacultyCalendarTitle']
            FacultyCalendarDesc=request.POST['FacultyCalendarDesc']
            FacultyCalendarStartDate=request.POST['FacultyCalendarStartDate']
            FacultyCalendarEndDate=request.POST['FacultyCalendarEndDate']
            FacultyCalendarLocation=request.POST['FacultyCalendarLocation']
            did=Department.objects.get(Did=request.POST['department']) 
            Image=request.FILES.get('Image',False)
           
            data=FacultyCalendarModel.objects.get(FacultyCalendarId=id)
            data.FacultyCalendarTitle=FacultyCalendarTitle
            data.FacultyCalendarDesc=FacultyCalendarDesc
            data.FacultyCalendarStartDate=FacultyCalendarStartDate
            data.FacultyCalendarEndDate=FacultyCalendarEndDate
            data.FacultyCalendarLocation=FacultyCalendarLocation
            data.Department_id=did
            if Image:
                data.Image=Image
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminfacultycalendar')

        data=FacultyCalendarModel.objects.get(FacultyCalendarId=id)
        did=data.Department_id.Did
        departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/admineditfacultycalendar.html',{'data':data,'department':departlist})
            
    except:
        return redirect('/university/')
    
def adminnotification(request):
    if request.method == "POST":
        NotificationTitle=request.POST['NotificationTitle']
        data=Admin_Notification.objects.filter(NotificationTitle__icontains=NotificationTitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminnotification.html',{'data':data})
    data=Admin_Notification.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-NotificationId')[:]
    return render(request,'uniadmin/adminnotification.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Admin_Notification.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminnotification.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
#adminnotificationSuggestion 
def adminnotificationSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Admin_Notification.objects.filter(NotificationTitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.NotificationId 
            project_json['value'] = project.NotificationTitle
            project_json['label'] = project.NotificationTitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)  

def adminaddnoti(request):
    try:
        if request.method=="POST":
            NotificationTitle=request.POST['NotificationTitle']
            NotificationDesc=request.POST['NotificationDesc']
            teacher=Instructor.objects.get(tid=request.POST['instructor']) 
            did=Department.objects.get(Did=request.POST['department']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Admin_Notification(NotificationTitle=NotificationTitle,NotificationDesc=NotificationDesc,uniId=uniid,branchId=branchid,Department_id=did,Instructor_id=teacher)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminnotification')
    
    except:
        return redirect('/university/')
    teacherlist=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddnoti.html',{'department':department,'teacherlist':teacherlist})
    
def deletenotificationmodel(request,id):
    try:
        data=Admin_Notification.objects.filter(NotificationId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminnotification')
    except:
        return redirect('/university/')

def Editnotificationmodel(request,id):
    try:
        if request.method=="POST":
            NotificationTitle=request.POST['NotificationTitle']
            NotificationDesc=request.POST['NotificationDesc']
            teacher=Instructor.objects.get(tid=request.POST['instructor']) 
            did=Department.objects.get(Did=request.POST['department']) 
            data=Admin_Notification.objects.get(NotificationId=id)
            data.NotificationTitle=NotificationTitle
            data.NotificationDesc=NotificationDesc
            data.Department_id=did
            data.Instructor_id=teacher
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminnotification')

    
        
        data=Admin_Notification.objects.get(NotificationId=id)
        did=data.Department_id.Did
        tid=data.Instructor_id.tid
        teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))

        return render(request,'uniadmin/Editnotificationmodel.html',{'data':data,'department':departlist,'teacherlist':teacherlist})
            
    except:
        return redirect('/university/')
    return render(request,'uniadmin/Editnotificationmodel.html')


def adminexam(request):
    if request.method == "POST":
        idslist=list()
        semester=Semester.objects.filter(Samester_Name__icontains=request.POST['semester'])
        for  ids in semester:
            idslist.append(ids.SamesterId)
        data=Exam_Schedule.objects.filter(Semester_ID__in=idslist,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminexam.html',{'data':data})
    data=Exam_Schedule.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Exam_Schedule_Id')[:]
    return render(request,'uniadmin/adminexam.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Exam_Schedule.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminexam.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
    
#adminexamSuggestion 
def adminexamSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Semester.objects.filter(Samester_Name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.SamesterId 
            project_json['value'] = project.Samester_Name
            project_json['label'] = project.Samester_Name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def addadminexam(request):
    try:
        if request.method=="POST":
            Year=request.POST['Year']
            Exam_Schedule_File=request.FILES['Exam_Schedule_File']
            semester=Semester.objects.get(SamesterId=request.POST['semester']) 
            did=Department.objects.get(Did=request.POST['depart']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Exam_Schedule(Year=Year,Exam_Schedule_File=Exam_Schedule_File,uniId=uniid,branchId=branchid,Department_id=did,Semester_ID=semester)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminexam')
    
    except:
        return redirect('/university/')
    semester=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/addadminexam.html',{'department':department,'semester':semester})
    
def deleteadminexam(request,id):
    try:
        data=Exam_Schedule.objects.filter(Exam_Schedule_Id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminexam')
    except:
        return redirect('/university/')

def admineditexam(request,id):
    try:
        if request.method=="POST":
            Year=request.POST['Year']
            Exam_Schedule_File=request.FILES.get('Exam_Schedule_File',False)
          
            semester=Semester.objects.get(SamesterId=request.POST['semester']) 
            did=Department.objects.get(Did=request.POST['depart']) 
            data=Exam_Schedule.objects.get(Exam_Schedule_Id=id)
            data.Year=Year
            data.Department_id=did
            data.Semester_ID=semester
            if Exam_Schedule_File:
                data.Exam_Schedule_File=request.FILES['Exam_Schedule_File']
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminexam')

            

        data=Exam_Schedule.objects.get(Exam_Schedule_Id=id)
        did=data.Department_id.Did
        semesterName=data.Semester_ID.SamesterId
        semester=Semester.objects.order_by(Case(When(Samester_Name=semesterName,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/admineditexam.html',{'department':departlist,'semester':semester,'data':data})
        
       
            
    except:
        return redirect('/university/')
    return render(request,'uniadmin/admineditexam.html')
   


def adminsemester(request):
    if request.method == "POST":
        ids=list()
        semester=Semester.objects.filter(Samester_Name__icontains=request.POST['semester'])
        for getid in semester:
            ids.append(getid.SamesterId)
        data=Semester_Schedule.objects.filter(Semester_ID__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminsemester.html',{'data':data})
    data=Semester_Schedule.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Semester_Schedule_Id')[:]
    return render(request,'uniadmin/adminsemester.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Semester_Schedule.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminsemester.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
    
    
#adminsemesterSuggestion 
def adminsemesterSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Semester.objects.filter(Samester_Name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.SamesterId 
            project_json['value'] = project.Samester_Name
            project_json['label'] = project.Samester_Name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 
def adminaddsemesterexm(request):
    try:
        if request.method=="POST":
            Year=request.POST['Year']
            Semester_Schedule_File=request.FILES['Semester_Schedule_File']
            semester=Semester.objects.get(SamesterId=request.POST['semester']) 
            did=Department.objects.get(Did=request.POST['depart']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=Semester_Schedule(Year=Year, Semester_Schedule_File=Semester_Schedule_File,uniId=uniid,branchId=branchid,Department_id=did,Semester_ID=semester)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminsemester')
    
    except:
        return redirect('/university/')
    semester=Semester.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddsemesterexm.html',{'department':department,'semester':semester})
    

def deleteadminsemester(request,id):
    try:
        data=Semester_Schedule.objects.filter(Semester_Schedule_Id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminsemester')
    except:
        return redirect('/university/')

def admineditsemeterexm(request,id):
    try:
        if request.method=="POST":
            Year=request.POST['Year']
                
            Semester_Schedule_File=request.FILES.get('Semester_Schedule_File',False)
           
            semester=Semester.objects.get(SamesterId=request.POST['semester']) 
            did=Department.objects.get(Did=request.POST['depart']) 
            data=Semester_Schedule.objects.get(Semester_Schedule_Id=id)
            data.Year=Year
            data.Department_id=did
            data.Semester_ID=semester
            if Semester_Schedule_File:
                data.Semester_Schedule_File=Semester_Schedule_File
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminsemester')

        data=Semester_Schedule.objects.get(Semester_Schedule_Id=id)
        did=data.Department_id.Did
        semesterName=data.Semester_ID.SamesterId
        semester=Semester.objects.order_by(Case(When(Samester_Name=semesterName,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
                
        return render(request,'uniadmin/admineditsemeterexm.html',{'department':departlist,'semester':semester,'data':data})
    
        
        
       
            
    except:
        return redirect('/university/')
    return render(request,'uniadmin/admineditsemeterexm.html')
   

def adminfacultyattendance(request):
    if request.method == "POST":
        ids=list()
        teacher=Instructor.objects.filter(First_Name__icontains=request.POST['teacher'])
        for getid in teacher:
            ids.append(getid.tid)
        data=FacultyAttendence.objects.filter(Instructor_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminfacultyattendance.html',{'data':data})
    data=FacultyAttendence.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-FacultyAttendenceId')[:]
    return render(request,'uniadmin/adminfacultyattendance.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=FacultyAttendence.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminfacultyattendance.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
    
#adminfacultyattendanceSuggestion 
def adminfacultyattendanceSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Instructor.objects.filter(First_Name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.tid 
            project_json['value'] = project.First_Name
            project_json['label'] = project.First_Name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def adminaddfacultyatten(request):
    try:
        if request.method=="POST":
            FacultyAttendenceYear=request.POST['FacultyAttendenceYear']
            FacultyAttendenceMonth=request.POST['FacultyAttendenceMonth']
            FacultyAttendencePresent=request.POST['FacultyAttendencePresent']
            FacultyAttendenceAbsent=request.POST['FacultyAttendenceAbsent']
            FacultyAttendenceTotal=request.POST['FacultyAttendenceTotal']
            teacher=Instructor.objects.get(tid=request.POST['teacher']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=FacultyAttendence(FacultyAttendenceYear=FacultyAttendenceYear,FacultyAttendenceMonth=FacultyAttendenceMonth,FacultyAttendencePresent=FacultyAttendencePresent,FacultyAttendenceAbsent=FacultyAttendenceAbsent,FacultyAttendenceTotal=FacultyAttendenceTotal,uniId=uniid,branchId=branchid,Instructor_id=teacher)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminfacultyattendance')
    
    except:
        return redirect('/university/')
    teacherlist=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddfacultyatten.html',{'teacherlist':teacherlist})
    
    
def deleteadminfacultyattendance(request,id):
    try:
        data=FacultyAttendence.objects.filter(FacultyAttendenceId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminfacultyattendance')
    except:
        return redirect('/university/')

def admineditfacultyattendance(request,id):
    try:
        if request.method=="POST":
            FacultyAttendenceYear=request.POST['FacultyAttendenceYear']
            FacultyAttendenceMonth=request.POST['FacultyAttendenceMonth']
            FacultyAttendencePresent=request.POST['FacultyAttendencePresent']
            FacultyAttendenceAbsent=request.POST['FacultyAttendenceAbsent']
            FacultyAttendenceTotal=request.POST['FacultyAttendenceTotal']
            teacher=Instructor.objects.get(tid=request.POST['teacher']) 
            data=FacultyAttendence.objects.get(FacultyAttendenceId=id)
            data.FacultyAttendenceYear=FacultyAttendenceYear
            data.FacultyAttendenceMonth=FacultyAttendenceMonth
            data.FacultyAttendencePresent=FacultyAttendencePresent
            data.FacultyAttendenceAbsent=FacultyAttendenceAbsent
            data.FacultyAttendenceTotal=FacultyAttendenceTotal
            data.Instructor_id=teacher
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminfacultyattendance')

        data=FacultyAttendence.objects.get(FacultyAttendenceId=id)
        tid=data.Instructor_id.tid
        month=data.FacultyAttendenceMonth
        monthname=FacultyAttendence.objects.order_by(Case(When(FacultyAttendenceMonth=month,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        teacherlist=Instructor.objects.order_by(Case(When(tid=tid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        return render(request,'uniadmin/admineditfacultyattendance.html',{'data':data,'teacherlist':teacherlist,'monthname':monthname})
       
            
    except:
        return redirect('/university/')
    return render(request,'uniadmin/admineditfacultyattendance.html')
    

def adminstudentattendance(request):
    if request.method == "POST":
        ids=list()
        student=Student_Profile.objects.filter(First_name__icontains=request.POST['student'])
        for getid in student:
            ids.append(getid.StudentId)
        data=StudentAttendence.objects.filter(Student_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminstudentattendance.html',{'data':data})
    data=StudentAttendence.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-StudentAttendenceId')[:]
    return render(request,'uniadmin/adminstudentattendance.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=StudentAttendence.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminstudentattendance.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
#adminstudentattendanceSuggestion 
def adminstudentattendanceSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Student_Profile.objects.filter(First_name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.StudentId 
            project_json['value'] = project.First_name
            project_json['label'] = project.First_name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def adminaddStudentatten(request):
    try:
        if request.method=="POST":
            StudentAttendenceYear=request.POST['StudentAttendenceYear']
            StudentAttendenceMonth=request.POST['StudentAttendenceMonth']
            StudentAttendencePresent=request.POST['StudentAttendencePresent']
            StudentAttendenceAbsent=request.POST['StudentAttendenceAbsent']
            StudentAttendenceTotal=request.POST['StudentAttendenceTotal']
            student=Student_Profile.objects.get(StudentId=request.POST['student']) 
            depart=Department.objects.get(Did=request.POST['depart']) 
            course=Course.objects.get(Cid=request.POST['course']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=StudentAttendence(StudentAttendenceYear=StudentAttendenceYear,StudentAttendenceMonth=StudentAttendenceMonth,StudentAttendencePresent=StudentAttendencePresent,StudentAttendenceAbsent=StudentAttendenceAbsent,StudentAttendenceTotal=StudentAttendenceTotal,uniId=uniid,branchId=branchid,Student_id=student,Department_id=depart,Course_id=course)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminstudentattendance')
   
        
    
    except:
        return redirect('/university/')
    student=Student_Profile.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddStudentatten.html',{'student':student,'department':department,'course':course})
    

def deleteadminstudentattendance(request,id):
    try:
        data=StudentAttendence.objects.filter(StudentAttendenceId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminstudentattendance')
    except:
        return redirect('/university/')


def admineditStudentattendance(request,id):
    try:
        if request.method=="POST":

            StudentAttendenceYear=request.POST['StudentAttendenceYear']
            StudentAttendenceMonth=request.POST['StudentAttendenceMonth']
            StudentAttendencePresent=request.POST['StudentAttendencePresent']
            StudentAttendenceAbsent=request.POST['StudentAttendenceAbsent']
            StudentAttendenceTotal=request.POST['StudentAttendenceTotal']
            student=Student_Profile.objects.get(StudentId=request.POST['student']) 
            depart=Department.objects.get(Did=request.POST['depart']) 
            course=Course.objects.get(Cid=request.POST['course']) 
            data=StudentAttendence.objects.get(StudentAttendenceId=id)
            data.StudentAttendenceYear=StudentAttendenceYear
            data.StudentAttendenceMonth=StudentAttendenceMonth
            data.StudentAttendencePresent=StudentAttendencePresent
            data.StudentAttendenceAbsent=StudentAttendenceAbsent
            data.StudentAttendenceTotal=StudentAttendenceTotal
            data.Department_id=depart
            data.Student_id=student
            data.Course_id=course
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminstudentattendance')

        data=StudentAttendence.objects.get(StudentAttendenceId=id)
        did=data.Department_id.Did
        cid=data.Course_id.Cid
        sid=data.Student_id.StudentId
        month=data.StudentAttendenceMonth
        monthname=StudentAttendence.objects.order_by(Case(When(StudentAttendenceMonth=month,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        departlist=Department.objects.order_by(Case(When(Did=did,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        courselist=Course.objects.order_by(Case(When(Cid=cid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))
        student=Student_Profile.objects.order_by(Case(When(StudentId=sid,then=0,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']),defeault=1))

    
        return render(request,'uniadmin/admineditStudentatten.html',{'data':data,'student':student,'department':departlist,'course':courselist,'monthname':monthname})
    
       
            
    except:
        return redirect('/university/')
    return render(request,'uniadmin/admineditStudentatten.html')
    




def adminfacultyevaluation(request):
    if request.method == "POST":
        Report_Name=request.POST['Report_Name']
        data=Faculty_Evaluation_Report.objects.filter(Report_Name__icontains=Report_Name,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminfacultyevaluation.html',{'data':data})
    
    data=Faculty_Evaluation_Report.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Faculty_Evaluation_Report_ID')[:]
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminfacultyevaluation.html',{'department':department,'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Faculty_Evaluation_Report.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     department=Department.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminfacultyevaluation.html',{'department':department,'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def addadminfacultyevaluation(request):
    if request.method=="POST":
        Report_Name=request.POST['Report_Name']
        Report_File=request.FILES['Report_File']
        depart=Department.objects.get(Did=request.POST['depart']) 
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=Faculty_Evaluation_Report(Report_Name=Report_Name,Report_File=Report_File,uniId=uniid,branchId=branchid,Department_id=depart)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminfacultyevaluation')
      
#adminfacultyevaluationSuggestion 
def adminfacultyevaluationSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Faculty_Evaluation_Report.objects.filter(Report_Name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.Faculty_Evaluation_Report_ID 
            project_json['value'] = project.Report_Name
            project_json['label'] = project.Report_Name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    
def deletefacultyevaluation(request,id):
    try:
        data=Faculty_Evaluation_Report.objects.filter(Faculty_Evaluation_Report_ID=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminfacultyevaluation')
    except:
        return redirect('/university/')

def show(request):

    userdata = list()
    id=request.GET['uid']
   
    request.session['facultyreport']=id
    
    data=Faculty_Evaluation_Report.objects.filter(Faculty_Evaluation_Report_ID=id)
    for x in data:
        datas=SerFaculty_Evaluation_Report(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))

def editadminfacultyevaluation(request):
    
    try:
        if request.method=="POST":
            Report_Name=request.POST['FReport_Name']
            depart=Department.objects.get(Did=request.POST['Fdepart']) 
            bid=request.session['facultyreport']
            data=Faculty_Evaluation_Report.objects.get(Faculty_Evaluation_Report_ID=bid)
            Report_File=request.FILES.get('FReport_File',False)
        
            if Report_File:
                data.Report_File=Report_File
            data.Report_Name=Report_Name
            data.Department_id=depart
            data.save()
            del request.session['facultyreport']
            messages.success(request,"Update Successfully")
            return redirect('adminfacultyevaluation')
            
        
    except:
        return redirect('/university/')


def adminform(request):
    if request.method == "POST":
        Formtitle=request.POST['Formtitle']
        data=Form.objects.filter(Formtitle__icontains=Formtitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminform.html',{'data':data})
    
    data=Form.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-FormId')[:]
    return render(request,'uniadmin/adminform.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Form.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminform.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def addadminform(request):
    if request.method=="POST":
        Formtitle=request.POST['Formtitle']
        FormFile=request.FILES['FormFile']
        FileCategory=request.POST['FileCategory']
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=Form(Formtitle=Formtitle,FormFile=FormFile,uniId=uniid,branchId=branchid,FileCategory=FileCategory)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminform')

#adminformSuggestion 
def adminformSuggestion(request):
    if not request.session.has_key('branchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Form.objects.filter(Formtitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.FormId 
            project_json['value'] = project.Formtitle
            project_json['label'] = project.Formtitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
def deleteadminform(request,id):
    try:
        data=Form.objects.filter(FormId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminform')
    except:
        return redirect('/university/')
def showform(request):
    userdata = list()
    id=request.GET['uid']
    request.session['formadmin']=id
    
    data=Form.objects.filter(FormId=id)
    for x in data:
        datas=SerForm(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))
   
  
def editadminform(request):
    
    try:
        if request.method=="POST":
            Formtitle=request.POST['FFormtitle']
            FileCategory=request.POST['FFileCategory']
            bid=request.session['formadmin']
            data=Form.objects.get(FormId=bid)
            FormFile=request.FILES.get('FFormFile',False)
            
            if FormFile:
                data.FormFile=FormFile
            data.Formtitle=Formtitle
            data.FileCategory=FileCategory
            data.save()
            del request.session['formadmin']
            messages.success(request,"Update Successfully")
            return redirect('adminform')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminform.html')


def adminrole(request):
    if request.method == "POST":
        ids=list()
        teacher=Instructor.objects.filter(First_Name__icontains=request.POST['teacher'])
        for getid in teacher:
            ids.append(getid.tid)
        data=role.objects.filter(Instructor_id__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        teacherlist=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminrole.html',{'data':data,'teacherlist':teacherlist})
    
    data=role.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-roleid')[:]
    teacherlist=Instructor.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminrole.html',{'data':data,'teacherlist':teacherlist})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=role.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     teacherlist=Instructor.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminrole.html',{'data':data,'teacherlist':teacherlist})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def addadminrole(request):
    if request.method=="POST":
        date=request.POST['date']
        active=request.POST['active']
        category=request.POST['category']
        teacher=Instructor.objects.get(tid=request.POST['teacher']) 
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=role(date=date,active=active,uniId=uniid,branchId=branchid,category=category,Instructor_id=teacher)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminrole')

#adminroleSuggestion 
def adminroleSuggestion(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Instructor.objects.filter(First_Name__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.tid 
            project_json['value'] = project.First_Name
            project_json['label'] = project.First_Name
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype) 

def deleteadminrole(request,id):
    try:
        data=role.objects.filter(roleid=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminrole')
    except:
        return redirect('/university/')

def showrole(request):
    userdata = list()
    id=request.GET['uid']
    request.session['roleadmin']=id
    
    data=role.objects.filter(roleid=id)
    for x in data:
        datas=Serrole(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))
   
  
def editrole(request):
    
    try:
        if request.method=="POST":
            teacher=Instructor.objects.get(tid=request.POST['Fteacher']) 
            category=request.POST['Fcategory']
            active=request.POST['Factive']
            date=request.POST['Fdate']
            bid=request.session['roleadmin']
            data=role.objects.get(roleid=bid)
            data.Instructor_id=teacher
            data.category=category
            data.active=active
            data.date=date
            data.save()
            del request.session['roleadmin']
            messages.success(request,"Update Successfully")
            return redirect('adminrole')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminrole.html')

def adminroom(request):
    if request.method == "POST":
        RoomName=request.POST['RoomName']
        data=Rooms.objects.filter(RoomName__icontains=RoomName,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminroom.html',{'data':data})
    
    
    data=Rooms.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-RoomId')[:]
    return render(request,'uniadmin/adminroom.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Rooms.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminroom.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def addadminroom(request):
    if request.method=="POST":
        RoomName=request.POST['RoomName']
        RoomCode=request.POST['RoomCode']
        RoomStatus=request.POST['RoomStatus']
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=Rooms(RoomName=RoomName,RoomCode=RoomCode,uniId=uniid,branchId=branchid,RoomStatus=RoomStatus)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminroom')


#Suggestionadminroom 
def Suggestionadminroom(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Rooms.objects.filter(RoomName__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.RoomId 
            project_json['value'] = project.RoomName
            project_json['label'] = project.RoomName
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def deleteadminroom(request,id):
    try:
        data=Rooms.objects.filter(RoomId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminroom')
    except:
        return redirect('/university/')

def showroom(request):
    userdata = list()
    id=request.GET['uid']
    request.session['roomadmin']=id
    
    data=Rooms.objects.filter(RoomId=id)
    for x in data:
        datas=Serroom(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))
   
  
def editroom(request):
    
    try:
        if request.method=="POST":
            
            RoomName=request.POST['FRoomName']
            RoomCode=request.POST['FRoomCode']
            RoomStatus=request.POST['FRoomStatus']
            bid=request.session['roomadmin']
            data=Rooms.objects.get(RoomId=bid)
            data.RoomName=RoomName
            data.RoomCode=RoomCode
            data.RoomStatus=RoomStatus
            data.save()
            del request.session['roomadmin']
            messages.success(request,"Update Successfully")
            return redirect('adminroom')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminrole.html')

def adminplacementportal(request):

    if request.method == "POST":
        Job_Title=request.POST['Job_Title']
        data=Placement_Portal.objects.filter(Job_Title__icontains=Job_Title,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminplacementportal.html',{'data':data})
    data=Placement_Portal.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-Placement_Portal_id')[:]
    return render(request,'uniadmin/adminplacementportal.html',{'data':data})
    
    

    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=Placement_Portal.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminplacementportal.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
        
   
    
def addadminplacementportal(request):
    if request.method=="POST":
        Job_Title=request.POST['Job_Title']
        Name_of_Organization=request.POST['Name_of_Organization']
        Company_Profile=request.POST['Company_Profile']
        Employment_Type=request.POST['Employment_Type']
        Jobdescription=request.FILES['Jobdescription']
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=Placement_Portal(Job_Title=Job_Title,Name_of_Organization=Name_of_Organization,uniId=uniid,branchId=branchid,Company_Profile=Company_Profile,Employment_Type=Employment_Type,Job_description=Jobdescription)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminplacementportal')
#Suggestionadminplacementportal 
def Suggestionadminplacementportal(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Placement_Portal.objects.filter(Job_Title__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.Placement_Portal_id 
            project_json['value'] = project.Job_Title
            project_json['label'] = project.Job_Title
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def deleteadminplacementportal(request,id):
    try:
        data=Placement_Portal.objects.filter(Placement_Portal_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminplacementportal')
    except:
        return redirect('/university/')

def showplacementportal(request):
    userdata = list()
    id=request.GET['uid']
    request.session['placement']=id
    
    data=Placement_Portal.objects.filter(Placement_Portal_id=id)
    for x in data:
        datas=SerPlacement_Portal(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))
   
  
def editadminplacementportal(request):
    
    try:
        if request.method=="POST":
            
            Job_Title=request.POST['FJob_Title']
            Name_of_Organization=request.POST['FName_of_Organization']
            Company_Profile=request.POST['FCompany_Profile']
            Employment_Type=request.POST['FEmployment_Type']
            Job_description=request.FILES.get('FJobdescription',False)
            
            bid=request.session['placement']
            data=Placement_Portal.objects.get(Placement_Portal_id=bid)
            data.Job_Title=Job_Title
            data.Name_of_Organization=Name_of_Organization
            data.Company_Profile=Company_Profile
            data.Employment_Type=Employment_Type
            if Job_description:
                data.Job_description=Job_description
            data.save()
            del request.session['placement']
            messages.success(request,"Update Successfully")
            return redirect('adminplacementportal')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminplacementportal.html')
    

def adminmenuitem(request):
    if request.method == "POST":
        MenuTitle=request.POST['MenuTitle']
        data=menu.objects.filter(MenuTitle__icontains=MenuTitle,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminmenuitem.html',{'data':data})
    
    
    
    data=menu.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-MenuId')[:]
    return render(request,'uniadmin/adminmenuitem.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=menu.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminmenuitem.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')

def addadminmenuitem(request):
    if request.method=="POST":
        MenuTitle=request.POST['MenuTitle']
        MenuType=request.POST['MenuType']
        uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
        branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
        data=menu(MenuTitle=MenuTitle,MenuType=MenuType,uniId=uniid,branchId=branchid)
        data.save()
        messages.success(request,"Successfully Added")
        return redirect('adminmenuitem')


#Suggestionadminmenuitem 
def Suggestionadminmenuitem(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = menu.objects.filter(MenuTitle__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.MenuId 
            project_json['value'] = project.MenuTitle
            project_json['label'] = project.MenuTitle
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
        
 
def deleteadminmenuitem(request,id):
    try:
        data=menu.objects.filter(MenuId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminmenuitem')
    except:
        return redirect('/university/')

def showmenu(request):
    userdata = list()
    id=request.GET['uid']
    request.session['menuadmin']=id
    
    data=menu.objects.filter(MenuId=id)
    for x in data:
        datas=Sermenu(x)
           
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))
   
  
def editadminmenuitem(request):
    
    try:
        if request.method=="POST":
            MenuTitle=request.POST['FMenuTitle']
            MenuType=request.POST['FMenuType']
            bid=request.session['menuadmin']
            data=menu.objects.get(MenuId=bid)
            data.MenuTitle=MenuTitle
            data.MenuType=MenuType
            data.save()
            del request.session['menuadmin']
            messages.success(request,"Update Successfully")
            return redirect('adminmenuitem')
        
    except:
        return redirect('/university/')
    return render(request,'uniadmin/adminmenuitem.html')
   
def adminmenuorder(request):
    if request.method == "POST":
        OrderList=request.POST['OrderList']
        data=MenuOrders.objects.filter(Q(OrderList__icontains=OrderList)|Q(OrderParticipants__icontains=OrderList),uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminmenuorder.html',{'data':data})
    data=MenuOrders.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-OrderId')[:]
    return render(request,'uniadmin/adminmenuorder.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=MenuOrders.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminmenuorder.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#Suggestionadminmenuorder 
def Suggestionadminmenuorder(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = MenuOrders.objects.filter(OrderList__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.OrderId 
            project_json['value'] = project.OrderList
            project_json['label'] = project.OrderList
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)       
    
    

def adminaddorder(request):
    try:
        if request.method=="POST":
            OrderParticipants=request.POST['OrderParticipants']
            OrderComments=request.POST['OrderComments']
            OrderList=request.POST['OrderList']
            OrderStartDate=request.POST['OrderStartDate']
            OrderStartTime=request.POST['OrderStartTime']
            OrderEndDate=request.POST['OrderEndDate']
            OrderEndTime=request.POST['OrderEndTime']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=MenuOrders(OrderParticipants=OrderParticipants,OrderComments=OrderComments,OrderList=OrderList,OrderStartDate=OrderStartDate,OrderStartTime=OrderStartTime,uniId=uniid,branchId=branchid,OrderEndTime=OrderEndTime,OrderEndDate=OrderEndDate)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminmenuorder')
  
    except:
        return redirect('/university/')
    
    return render(request,'uniadmin/adminaddorder.html')
  
def deletemenuorder(request,id):
    try:
        data=MenuOrders.objects.filter(OrderId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminmenuorder')
    except:
        return redirect('/university/')

def admineditorder(request,id):
    try:
        if request.method=="POST":

            OrderParticipants=request.POST['OrderParticipants']
            OrderComments=request.POST['OrderComments']
            OrderList=request.POST['OrderList']
            OrderStartDate=request.POST['OrderStartDate']
            OrderStartTime=request.POST['OrderStartTime']
            OrderEndDate=request.POST['OrderEndDate']
            OrderEndTime=request.POST['OrderEndTime']
            data=MenuOrders.objects.get(OrderId=id)
            data.OrderParticipants=OrderParticipants
            data.OrderComments=OrderComments
            data.OrderList=OrderList
            data.OrderStartDate=OrderStartDate
            data.OrderStartTime=OrderStartTime
            data.OrderEndDate=OrderEndDate
            data.OrderEndTime=OrderEndTime
            
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminmenuorder')
        data=MenuOrders.objects.filter(OrderId=id)
        
        return render(request,'uniadmin/admineditorder.html',{'data':data})
    
       
    except:
        return redirect('/university/')
 
    
def adminroomreservation(request):
    if request.method == "POST":
        ids=list()
        room=Rooms.objects.filter(RoomName__icontains=request.POST['room'])
        for idlist in room:
            ids.append(idlist.RoomId)
        data=RoomReservation.objects.filter(RoomId__in=ids,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminroomreservation.html',{'data':data})
    data=RoomReservation.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-ReservationId')[:]
    return render(request,'uniadmin/adminroomreservation.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=RoomReservation.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminroomreservation.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
#Suggestionadminroomreservation 
def Suggestionadminroomreservation(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = Rooms.objects.filter(RoomName__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.RoomId 
            project_json['value'] = project.RoomName
            project_json['label'] = project.RoomName
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)              
    
    

def adminaddroomres(request):
    try:
        if request.method=="POST":
            ReservationParticipants=request.POST['ReservationParticipants']
            ReservationComments=request.POST['ReservationComments']
            ReservationStartDate=request.POST['ReservationStartDate']
            ReservationStartTime=request.POST['ReservationStartTime']
            ReservationEndDate=request.POST['ReservationEndDate']
            ReservationEndTime=request.POST['ReservationEndTime']
            room=Rooms.objects.get(RoomId=request.POST['room']) 
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=RoomReservation(ReservationParticipants=ReservationParticipants,ReservationComments=ReservationComments,ReservationStartDate=ReservationStartDate,ReservationStartTime=ReservationStartTime,ReservationEndDate=ReservationEndDate,uniId=uniid,branchId=branchid,ReservationEndTime=ReservationEndTime,RoomId=room)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminroomreservation')
  
    except:
        return redirect('/university/')
    room=Rooms.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'uniadmin/adminaddroomres.html',{'room':room})

def deleteadminroomreservation(request,id):
    try:
        data=RoomReservation.objects.filter(ReservationId=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminroomreservation')
    except:
        return redirect('/university/')  

def admineditroomreservation(request,id):
    try:
        if request.method=="POST":

            ReservationParticipants=request.POST['ReservationParticipants']
            ReservationComments=request.POST['ReservationComments']
            ReservationStartDate=request.POST['ReservationStartDate']
            ReservationStartTime=request.POST['ReservationStartTime']
            ReservationEndDate=request.POST['ReservationEndDate']
            ReservationEndTime=request.POST['ReservationEndTime']
            room=Rooms.objects.get(RoomId=request.POST['room']) 
            data=RoomReservation.objects.get(ReservationId=id)
            data.ReservationParticipants=ReservationParticipants
            data.ReservationComments=ReservationComments
            data.ReservationStartDate=ReservationStartDate
            data.ReservationStartTime=ReservationStartTime
            data.ReservationEndDate=ReservationEndDate
            data.ReservationEndTime=ReservationEndTime
            data.RoomId=room
            
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminroomreservation')
        data=RoomReservation.objects.filter(ReservationId=id)
        room=Rooms.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/admineditroomreservation.html',{'data':data,'room':room})
    
       
    except:
        return redirect('/university/')
    



def adminsurvery(request):
    if request.method == "POST":
        question_1=request.POST['question_1']
        data=onlinesurvey.objects.filter(question_1__icontains=question_1,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
        return render(request,'uniadmin/adminsurvery.html',{'data':data})
    data=onlinesurvey.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid']).order_by('-onlinesurvey_id')[:]
    return render(request,'uniadmin/adminsurvery.html',{'data':data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()
  
    # data=UniversityBranch.objects.get(BranchId=request.session['branchid'])
    # past=data.UniversityId.UniPackage.PackDurationEnd
    # unidata=UniversityAccount.objects.get(UniId=request.session['uniid'])
 
    # if past >= present and unidata.UniStatus == "Active":
    #     data=onlinesurvey.objects.filter(uniId=request.session['uniid'],branchId=request.session['branchid'])
    #     return render(request,'uniadmin/adminsurvery.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')
    
        
#Suggestionadminroomreservation 
def Suggestionadminsurvery(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        projects = onlinesurvey.objects.filter(question_1__istartswith=q)[:5]
        results = []
        for project in projects:
            project_json = {}
            project_json['id'] = project.onlinesurvey_id 
            project_json['value'] = project.question_1
            project_json['label'] = project.question_1
            results.append(project_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)             
    

def adminaddsurvey(request):
    try:
        if request.method=="POST":
            question_1=request.POST['question_1']
            question_2=request.POST['question_2']
            question_3=request.POST['question_3']
            uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
            branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
            data=onlinesurvey(uniId=uniid,branchId=branchid,question_1=question_1,question_2=question_2,question_3=question_3)
            data.save()
            messages.success(request,"Successfully Added")
            return redirect('adminsurvery')
  
    except:
        return redirect('/university/')
    
    return render(request,'uniadmin/adminaddsurvey.html')
    

def deleteadminsurvery(request,id):
    try:
        data=onlinesurvey.objects.filter(onlinesurvey_id=id)
        data.delete()
        messages.error(request,"Delete Sucessfully")
        return redirect('adminsurvery')
    except:
        return redirect('/university/')  
def admineditsurvey(request,id):
    try:
        if request.method=="POST":

            question_1=request.POST['question_1']
            question_2=request.POST['question_2']
            question_3=request.POST['question_3']
            data=onlinesurvey.objects.get(onlinesurvey_id=id)
            data.question_1=question_1
            data.question_2=question_2
            data.question_3=question_3
            data.save()
            messages.success(request,"Update Successfully")
            return redirect('adminsurvery')
        data=onlinesurvey.objects.filter(onlinesurvey_id=id)
        return render(request,'uniadmin/admineditsurvey.html',{'data':data})
    
    except:
        return redirect('/university/')
    

# add batch section by shoaib ghulam
def adminbatch(request):
    
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    
    uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
    branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
     
    if request.method == "POST":
        batchname=request.POST['batch']
        query=Batch.objects.filter(Batch_Name=batchname)
        if query:
            messages.error(request,"Batch Name is Already Inserted")
            return redirect("adminbatch")
        else:
            batchdata=Batch(Batch_Name=batchname,uniId=uniid,branchId=branchid)
            batchdata.save()
            messages.success(request,'Batach has been Inserted')
            return redirect('adminbatch')

          
    data=Batch.objects.filter(uniId=uniid,branchId=branchid)
    return render(request,'uniadmin/adminbatch.html',{'data':data})

    # get batch data through ajax
def getbatchdata(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    
    uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
    branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
    if request.method == "GET":
            
        id=request.GET['id']
        data=Batch.objects.filter(Batch_id=id,uniId=uniid,branchId=branchid)[0]
       
        serdata=Ser_Batch(data , many=False)
        
        return HttpResponse(json.dumps(serdata.data))
    if request.method =="POST":
        uid=request.POST['uid']
        ubatch=request.POST['ubatch']
        udata = Batch.objects.get(Batch_id=uid,uniId=uniid,branchId=branchid)
        udata.Batch_Name=ubatch
        udata.save()
        messages.success(request,"Batch has been Update")
        return redirect('adminbatch')

def deletebatch(request ,id):
     if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
     uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
     branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
     deldata=Batch.objects.get(Batch_id=id,uniId=uniid,branchId=branchid)
     deldata.delete()
     messages.error(request,"Batch has been Deleted")
     return redirect('adminbatch')


def searchbatch(request):
    if not request.session.has_key('universitybranchid'):
        return redirect('/university/login')
    uniid=UniversityAccount.objects.get(UniId=request.session['universityuniid'])
    branchid=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])   
    query=request.POST.get('query','Batch')
    data=Batch.objects.filter(Batch_Name__icontains=query,uniId=uniid,branchId=branchid)
    return render(request,'uniadmin/adminbatch.html',{'data':data})
    # return rredirect('adminbatch'),{'data':data})

    
# send credentials to student login user and password  by shoaib ghulam
def studentcredentials(request,id):
    data=Student_Signup.objects.get(user_id=id,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    # uniname=UniversityBranch.objects.get(request.session['universityuniid']
    unidata=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
    uniuser=unidata.UniversityId.UniUsername
    branchuser=unidata.BranchUsername
    subject=f"Login Credential {unidata.BranchName}"
    url=f"http://127.0.0.1/studentlogin/{uniuser}/{branchuser}";
    # email tamplate start
    subject, from_email, to = subject, 'test@certnetworks.tk', data.email
    html_content = f'''
            <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Login Credential {unidata.BranchName}</h1>
                <p>
                  Username:  {data.email} <br>
                  password: {data.password}
                  </p>
            <div style='width:300px; margin:0 auto;'> <a href='{url}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
        </div>
            '''
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # email tamplate end
    messages.success(request,"Credential has been sent")
    return redirect('/university/adminsignup')





# send credentials to Faculty login user and password
def facultycredentials(request,id):
    data=User_Signup.objects.get(user_id=id,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    unidata=UniversityBranch.objects.get(BranchId=request.session['universitybranchid'])
    uniuser=unidata.UniversityId.UniUsername
    branchuser=unidata.BranchUsername
    subject=f"Login Credential {unidata.BranchName}"
    url=f"http://127.0.0.1/Facultylogin/{uniuser}/{branchuser}";
    # email tamplate start
    subject, from_email, to = subject, 'test@certnetworks.tk', data.email
    html_content = f'''
            <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Login Credential {unidata.BranchName}</h1>
                <p>
                  Username:  {data.email} <br>
                  password: {data.password}
                  </p>
            <div style='width:300px; margin:0 auto;'> <a href='{url}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
        </div>
            '''
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # email tamplate end
    messages.success(request,"Credential has been sent")
    return redirect('/university/adminsignup')

# send credentials to Faculty login user and password

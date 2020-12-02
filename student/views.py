from django.shortcuts import render,HttpResponse,redirect
from student.models import Student_Course,Student_Profile,Student_Signup,SerStudent,Application,Student_Query_Admin,Student_Survey,Registration,ScrunityForm,Job_Apply,Student_Submit_Evaluation,MeetingAppointment,Student_Assigment,Ser_Assigment,Ser_App,SerMeeting,Student_Midterm,Ser_Midterms,Student_FinalExam,Ser_FinalExams
from faculty.models import Course,Materialclass,AssigmentModel,NotificationModel,CourseVideos,Faculty_Evaluation,Semester,Exam_Result,Department,onlinequiz,Ser_AssigmentStudent,MidtermModel,FinalExamModel,Ser_FinalExam,Ser_Midterm
from administrator.models import AcademicCalendarModel,Form,StudentAttendence,Exam_Schedule,onlinesurvey,Semester_Schedule,Placement_Portal
from library.models import Books,BookAuthor
from django.core.paginator import Paginator
from UniversityApp.models import UniversityAccount,UniversityBranch
import json
from django.db.models import Q
import pandas as pd
from urllib.request import urlopen
from django.contrib import messages
from datetime import datetime

# Create your views here.
def studentdashboard(request): 
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            return render(request,'student/page-dashboard-student.html',{'student_signupname':student_signupname})
           
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
        


def examresultstudent(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            id=student.StudentId
            data=Exam_Result.objects.filter(Student_ID=id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-Exam_Result_id')[:] 
            return render(request,'student/examresultstudent.html',{'data':data})
           
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
          
    except:
        return redirect('/')



def registration(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid']) 
           
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        
            depart = student.Department_id.Did

            course_data = Course.objects.filter(Department_id = depart,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            firstname=student.First_name
            lastname=student.Last_name
            Reg=Registration.objects.get(Student_id=student)
            regno=Reg.Student_Registration_Code
            program=Reg.Student_Program
            return render(request,'student/registration.html',{'firstname':firstname,'lastname':lastname,'regno':regno,'program':program,'course':course_data})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

            
            
    except:
        return redirect('/')
  
        

    # except:
    #     return redirect('/student/')



def transcript(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            data=Exam_Result.objects.filter(Student_ID=Student_Profile.objects.get(User_id=student_signupname.user_id)).order_by('-Exam_Result_id')[:] 
            print(data)
            return render(request,'student/transcript.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
        

def studentcalendar(request):
    try:
        if request.session['role']=="Student":
            data=AcademicCalendarModel.objects.filter(uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-AcademicCalendarId')[:]
            return render(request,'student/studentcalendar.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
        
         

def curriculum(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            depart = student.Department_id.Did
            course_data = Course.objects.filter(Department_id = depart,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            firstname=student.First_name
            lastname=student.Last_name
            Reg=Registration.objects.get(Student_id=student.StudentId)
            regno=Reg.Student_Registration_Code
            program=Reg.Student_Program
            return render(request,'student/curriculum.html',{'firstname':firstname,'lastname':lastname,'regno':regno,'program':program,'course':course_data})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
            
            
    except:
        return redirect('/')
 
def library(request):
    # libary html page data
    try:
        if request.session['role']=="Student":
            datas= Books.objects.filter(uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-BookId')
            paginator = Paginator(datas,5)
            pages=request.GET.get('page',5)
            pagenumber= paginator.get_page(pages)
            if pagenumber.has_next():
                next_url=f'?page={pagenumber.next_page_number()}'
            else:
                next_url=''

            if pagenumber.has_previous():
                previous_url=f'?page={ pagenumber.previous_page_number() }'
            else:
                previous_url=''    
            alldata={
                'data':pagenumber,
                'nextpage':next_url,
                'previouspage':previous_url,
            }
            # end library page data
            if request.method=="POST":
                books=request.POST['BookTitle']
                BookAuthorName=request.POST['BookAuthor']
                BookPublisher=request.POST['BookPublisher']
                BookIsbn=request.POST['BookIsbn']
                if books:
                    data=Books.objects.filter(Q(BookTitle__icontains=books))
                if BookAuthorName:
                    ids=list()
                    author=BookAuthor.objects.filter(Q(BookAuthorFirstName__icontains=BookAuthorName)|Q(BookAuthorLastName__icontains=BookAuthorName))
                    for getid in author:
                        ids.append(getid.BookAuthorId)

                    data=Books.objects.filter(BookAuthorid__in=ids)
                if BookPublisher:
                    data=Books.objects.filter(Q(BookPublisher__icontains=BookPublisher))
                if BookIsbn:
                    data=Books.objects.filter(Q(BookISBN__icontains=BookIsbn))

                alldata={
                    'data':data
                }
                return render(request,'student/librarysearch.html',alldata)
        
        
            return render(request,'student/library.html',alldata) 

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')


def digitallibrary(request):

    # try:
    if request.session['role']=="Student":
        if request.method == "POST":
            BookTitle=request.POST['BookTitle']
            data=Books.objects.filter(Bookcategory="digitallibrary",BookTitle=BookTitle,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            return render(request,'student/digitallibrary.html',{'data':data})
        data= Books.objects.filter(Bookcategory="digitallibrary",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-BookId')[:]
        return render(request,'student/digitallibrary.html',{'data':data})
          
    # else:
    #     thank=True
    #     msg='Your are not a Student'
    #     return render(request,'index.html',{'thank':thank,'msg':msg})
             
    # except:
    #     return redirect('/')


def suggestiondigitallibrary(request):
    
    
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Books.objects.filter(Bookcategory="digitallibrary",BookTitle__istartswith=q)[:5]
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
def Phddigitallibrary(request):
    # try:
    if request.session['role']=="Student":

        if request.method == "POST":
            BookTitle=request.POST['BookTitle']
            data=Books.objects.filter(Bookcategory="digitallibraryphd",BookTitle=BookTitle,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            return render(request,'student/Phddigitallibrary.html',{'data':data})
        data= Books.objects.filter(Bookcategory="digitallibraryphd",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-BookId')[:]
        return render(request,'student/Phddigitallibrary.html',{'data':data})
            
    else:
        thank=True
        msg='Your are not a Student'
        return render(request,'index.html',{'thank':thank,'msg':msg})
             
    # except:
    #     return redirect('/')


def suggesPhddigitallibrary(request):
    
    
    if request.is_ajax():
        q = request.GET.get('term', '')
        print(q)
        
        projects = Books.objects.filter(Bookcategory="digitallibraryphd",BookTitle__istartswith=q)[:5]
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
def onlinelecture(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=Materialclass.objects.filter(Course_id=course_id.Cid,Category="lectures").order_by('-Materailid')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/onlinelecture.html',{'course':data,'data':courses})
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/onlinelecture.html',{'data':courses})
        
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')


def fvledashboard(request):
    try:
        if request.session['role']=="Student":
            return render(request,'student/vledashboard.html')
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
        



def myclass(request):
    try:
        if request.session['role']=="Student":
            return render(request,'student/myclass.html')
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
        

def classmaterial(request):
    try:
        if request.session['role']=="Student":
            return render(request,'student/classmaterial.html')
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
       
    

def Onlinequiz(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            a=courses.values_list('Courses', flat=True)
            data=onlinequiz.objects.filter(Course_id__in=a,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-onlinequizid')[:] 
            return render(request,'student/onlinequiz.html',{'data':data})
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')


def startquiz(request):
    return render(request,'student/startquiz.html')

    

        
 


def studentprofile(request):
    # try:
        if request.session['role']=="Student":
            if request.method=="POST":
                img=request.FILES.get('image',False)
                firstname=request.POST['firstname']
                lastname=request.POST['lastname']
                batch=request.POST['batch']
                address=request.POST['address']
                phone=request.POST['phone']
                birth=request.POST['birth']
                shift=request.POST['shift']
                username=request.session['username']
                
                user=Student_Signup.objects.get(username=username,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
                
                data=Student_Profile.objects.get(User_id=request.session['userid'])

                data.First_name=firstname
                data.Last_name=lastname
                data.ContactNo=phone
                data.Address=address
                data.DOB=birth
                data.StudenShift=shift
                if img:
                    data.Profile=img
                data.save()
                images=Student_Profile.objects.get(User_id=request.session['userid'])
                request.session['senderimg']= str(images.Profile)
                        
                thank=True
                msg="Your Profile Sucessfully update"
                return HttpResponse(msg)
                # return render(request,'student/page-dashboard-student.html',{'thank':thank,'msg':msg})
            
            username=request.session['username']
            user=Student_Signup.objects.get(username=username,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            data=Student_Profile.objects.filter(User_id=user,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            if data:
                thank=True
                return render(request,'student/studentprofile.html',{'thank':thank})
            else:
                thank=False
                return render(request,'student/studentprofile.html',{'thank':thank})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    # except:
    #     # return redirect('/')
    #     return HttpResponse("hello")
    
    
def showstudent(request):
   
    try:
        if request.session['role']=="Student":
            userdata = list()
            data=Student_Profile.objects.filter(User_id=Student_Signup.objects.get(username=request.session['username']),uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            if data:
                for x in data:
                    datas=SerStudent(x)
                    userdata.append(datas.data)
                return HttpResponse(json.dumps(userdata))
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

def editstudent(request):
    
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                data=Student_Profile.objects.filter(User_id=Student_Signup.objects.get(username=request.session['username'])).update(First_name=request.POST['firstname'],Last_name=request.POST['lastname'],ContactNo=request.POST['phone'],Address=request.POST['address'],DOB=request.POST['birth'],StudenBatch=request.POST['batch'],StudenShift=request.POST['shift'])
                return HttpResponse('Update Profile Suceesfully')
        

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
    


def allnotification(request):
    try:
        if request.session['role']=="Student":
            return render(request,'student/allnotification.html')
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
        

def video(request,id):
    try:
        if request.session['role']=="Student":
            data=CourseVideos.objects.filter(VideoId=id)
            return render(request,'student/videoshow.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
      
    except:
        return redirect('/')


# **************************************************Shoaib**************************************************************************
#OnlineBook

   
def onlinebook(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=Materialclass.objects.filter(Course_id=course_id.Cid,Category="ebooks",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-Materailid')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/onlinelecture.html',{'course':data,'data':courses})
    
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/onlinebook.html',{'data':courses})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')


def assignments(request):
    
    # try:
    if request.session['role']=="Student":

        if request.method=="POST":
            
            course_id=request.POST['courses']
            data=AssigmentModel.objects.filter(Course_id=course_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-AsssigmentId')[:] 
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            studentname=student.First_name
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            result = urlopen('http://just-the-time.appspot.com/')
            result = result.read().strip()
            result_str = result.decode('utf-8')
            present=result_str[:10]
            present = pd.to_datetime(present).date()
            return render(request,'student/assignments.html',{'course':data,'data':courses,'name':studentname,'present':present})
            # return render(request,'student/assignments.html',{'course':data,'data':courses,'name':studentname})

        student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
        student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        studentname=student.First_name
        courses=Student_Course.objects.filter(Student_ID=student.StudentId)
        a=courses.values_list('Courses', flat=True)

           

        data=AssigmentModel.objects.filter(Course_id__in=a,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'], Status="True")
        result = urlopen('http://just-the-time.appspot.com/')
        result = result.read().strip()
        result_str = result.decode('utf-8')
        present=result_str[:10]
        present = pd.to_datetime(present).date()
        print(present)
        return render(request,'student/assignments.html',{'data':courses,'name':studentname,'course':data,'present':present})

    #     else:
    #         thank=True
    #         msg='Your are not a Student'
    #         return render(request,'index.html',{'thank':thank,'msg':msg})      
        
    # except:
    #     return redirect('/')

def showstudentAssignment(request):
    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=AssigmentModel.objects.get(AsssigmentId=uid)
        mydata=Ser_AssigmentStudent(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))


  
def mygrade(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=Course.objects.filter(Cid=course_id.Cid,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-Cid')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/mygrade.html',{'course':data,'data':courses})

            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/mygrade.html',{'data':courses})
        
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')



def notification(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=NotificationModel.objects.filter(Course_id=course_id.Cid,Category="class",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-NotificationId')[:] 

                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/notification.html',{'course':data,'data':courses})
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/notification.html',{'data':courses})
    
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    
    except:
        return redirect('/')

def secnotification(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=NotificationModel.objects.filter(Course_id=course_id.Cid,Category="Section",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-NotificationId')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid']) 
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/secnotification.html',{'course':data,'data':courses})
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/secnotification.html',{'data':courses})
    
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
    

def programnotification(request):
    try:
        if request.session['role']=="Student":

            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=NotificationModel.objects.filter(Course_id=course_id.Cid,Category="program",uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-NotificationId')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/programnotification.html',{'course':data,'data':courses})
        
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/programnotification.html',{'data':courses})
    
    
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
    except:
        return redirect('/')



def mynotification(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=NotificationModel.objects.filter(Course_id=course_id.Cid,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-NotificationId')[:]
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/mynotification.html',{'course':data,'data':courses})
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/mynotification.html',{'data':courses})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
    
    
    
    except:
        return redirect('/')



def application(request):
    # try:
    if request.session['role']=="Student":
        if request.method=="POST":
            course_id=request.POST['courses']
         
            data=Application.objects.filter(Course_id=course_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-ApplicationId')[:] 
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/application.html',{'course':data,'data':courses})
        
        student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
        student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        courses=Student_Course.objects.filter(Student_ID=student.StudentId)
        return render(request,'student/application.html',{'data':courses})

    else:
        thank=True
        msg='Your are not a Student'
        return render(request,'index.html',{'thank':thank,'msg':msg})
    
    # except:
    #      return redirect('/')

def teacherreply(request):
    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Application.objects.get(ApplicationId=uid)
        mydata=Ser_App(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

def createapplication(request):
    try:
        if request.session['role']=="Student":
   
            if request.method=="POST":
                ApplicationTitle=request.POST['ApplicationTitle']
                ApplicationMessage=request.POST['ApplicationMessage']
                ApplicationAttachment=request.FILES['ApplicationAttachment']
                course_id=Course.objects.get(Course_name=request.POST['courses'])
                id=course_id.Instructor_id
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
                
                data=Application(ApplicationTitle=ApplicationTitle,ApplicationMessage=ApplicationMessage,ApplicationAttachment=ApplicationAttachment,Course_id=course_id,Student_id=studentname,Instructor_id=id,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                data.save()
                thank=True
            
                # return render(request,'student/myclass.html',{'thank':thank,'msg':msg})
                messages.error(request,"Successfully Uploaded")
                return redirect('/student/application')
            
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/createapplication.html',{'data':courses})

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})    
    
    except:
        return redirect('/')
    
 

def onlinequery(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                course_name=request.POST['courses']
                course_id=Course.objects.get(Course_name=course_name)
                data=Student_Query_Admin.objects.filter(Course_id=course_id.Cid,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-queryid')[:] 
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
                courses=Student_Course.objects.filter(Student_ID=student.StudentId)
                return render(request,'student/onlinequery.html',{'course':data,'data':courses})
    
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/onlinequery.html',{'data':courses})
    
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg}) 
    
    except:
        return redirect('/')


def createquery(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                querytitle=request.POST['querytitle']
                querymessage=request.POST['querymessage']
                course_id=Course.objects.get(Course_name=request.POST['courses'])
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id)
                
                data=Student_Query_Admin(querytitle=querytitle,querymessage=querymessage,Course_id=course_id,Student_ID=studentname,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                data.save()
                thank=True
                messages.error(request,"Successfully Uploaded")
                return redirect('/student/onlinequery')
                


            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/createquery.html',{'data':courses})
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg}) 

    except:
        return redirect('/')
    
    
    
# ****Videos**********
def myroles(request):
    
    # try:
    if request.session['role']=="Student":
        if request.method=="POST":
            course_id=request.POST['courses']
            data=CourseVideos.objects.filter(CourseId=course_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-VideoId')[:]
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            return render(request,'student/myroles.html',{'course':data,'data':courses})
        
        
        student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
        student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        courses=Student_Course.objects.filter(Student_ID=student.StudentId)
        return render(request,'student/myroles.html',{'data':courses})
    
    
    #     else:
    #         thank=True
    #         msg='Your are not a Student'
    #         return render(request,'index.html',{'thank':thank,'msg':msg}) 

    # except:
    #      return redirect('/')



#semester form guidline
def formguidline(request):
    try:
        if request.session['role']=="Student":
            appform=Form.objects.filter(FileCategory="applicationform").order_by('-FormId')[:] 
            thesisform=Form.objects.filter(FileCategory="thesisguidline").order_by('-FormId')[:] 
            placeform=Form.objects.filter(FileCategory="placementforms").order_by('-FormId')[:] 
            
            return render(request,'student/formguidline.html',{'appform':appform,'thesisform':thesisform,'placeform':placeform})

            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
         
    except:
        return redirect('/')
   
    
 #semester facultyattendance
def studentattendance(request):
    try:
        if request.session['role']=="Student":
        

            if request.method=="POST":
                course_name=request.POST['courses']
                cid=Course.objects.get(Course_name=course_name)
                course_id=cid.Cid
                year=request.POST['Year']
                month=request.POST['Month']
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                student=Student_Profile.objects.get(User_id=student_signupname.user_id)
                    
                courses=Student_Course.objects.filter(Student_ID=student.StudentId) 
                attendence=StudentAttendence.objects.filter(Student_id=student.StudentId,Course_id=course_id,StudentAttendenceMonth=month,StudentAttendenceYear=year)
                return render(request,'student/studentattendance.html',{'data':courses,'attendence':attendence})
            
            
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)   
            attendence=StudentAttendence.objects.filter(Student_id=student.StudentId).order_by('-StudentAttendenceId')[:] 
            return render(request,'student/studentattendance.html',{'data':courses,'attendence':attendence})
        

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        
    
    except:
        return redirect('/')



def examschedule(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.get(Student_ID=student.StudentId)
            id=courses.Department_id
            data=Exam_Schedule.objects.filter(Department_id=id).order_by('-Exam_Schedule_Id')[:] 
            return render(request,'student/examschedule.html',{'data':data}) 
         
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

        
    except:
        return redirect('/')

   
def semesterschedule(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.get(Student_ID=student.StudentId)
            id=courses.Department_id
            data=Semester_Schedule.objects.filter(Department_id=id).order_by('-Semester_Schedule_Id')[:] 
            return render(request,'student/semesterschedule.html',{'data':data})   
   
  
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

          
    except:
        return redirect('/')

def survey(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                question_1_Answer=request.POST['question_1_Answer']
                question_2_Answer=request.POST['question_2_Answer']
                question_3_Answer=request.POST['question_3_Answer']
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id)
                    
                data=Student_Survey(question_1_Answer=question_1_Answer,question_2_Answer=question_2_Answer,question_3_Answer=question_3_Answer,Student_id=studentname,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid'])) 
                data.save()
                thank=True
                msg="Successfully Submitted Answers"
                return render(request,'student/page-dashboard-student.html',{'thank':thank,'msg':msg}) 

            survey=onlinesurvey.objects.filter(uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-onlinesurvey_id')[:]
            return render(request,'student/survey.html',{'survey':survey})

        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        
    
    except:
        return redirect('/')


   
def Scrunityform(request):
    try:
 
        if request.session['role']=="Student":

            if request.method=="POST":

                Student_Name=request.POST['Student_Name']
                Program=request.POST['Program']
                Registration_no=request.POST['Registration_no']
                Date=request.POST['Date']
                Scrunity_Rechecking=request.POST['Scrunity_Rechecking']
                Research_for_Evalution=request.POST['Research_for_Evalution']
                Voucher_Number=request.POST['Voucher_Number']
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id)
                course_id=Course.objects.get(Course_name=request.POST['courses'])
                data=ScrunityForm(Student_Name=Student_Name,Program=Program,Registration_no=Registration_no,Date=Date,Scrunity_Rechecking=Scrunity_Rechecking,Research_for_Evalution=Research_for_Evalution,Voucher_Number=Voucher_Number,Student_id=studentname,Course_id=course_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                data.save()
                thank=True
                msg="Successfully Submitted"
                return render(request,'student/page-dashboard-student.html',{'thank':thank,'msg':msg}) 

                
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            studentname=Student_Profile.objects.filter(StudentId=student.StudentId)
            register=Registration.objects.filter(Student_id=student.StudentId)
            return render(request,'student/Scrunityform.html',{'data':courses,'studentname':studentname,'register':register})   
            
        
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
        
    
    
    except:
        messages.error(request,"Please submit your Enrollment For rechecking")
        return redirect('/student/')


def placement(request):
    try:
        if request.session['role']=="Student":
            job=Placement_Portal.objects.filter(uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-Placement_Portal_id')[:] 
            return render(request,'student/placement.html',{'job':job})
           
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')


def jobapply(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                Student_Name=request.POST['Student_Name']
                Program=request.POST['Program']
                Job_Experirnce=request.POST['Experirence']
                Cv=request.FILES['Cv']
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id)
                data=Job_Apply(Student_Name=Student_Name,Program=Program,Student_id=studentname,Job_Experirnce=Job_Experirnce,Cv=Cv,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                
                data.save()
                thank=True
                messages.success(request,"Applied successfuly")
                return redirect('/student/placement')


            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            register=Registration.objects.filter(Student_id=student.StudentId)
            studentname=Student_Profile.objects.filter(StudentId=student.StudentId)
            return render(request,'student/jobapply.html',{'studentname':studentname,'register':register})
        
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')

def facultyevaluations(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.get(Student_ID=student.StudentId)   
            faculty=Faculty_Evaluation.objects.filter(Department_id=courses.Department_id).order_by('-Faculty_Evaluation_ID')[:] 
            return render(request,'student/facultyevaluations.html',{'faculty':faculty})
           
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
           
    except:
        return redirect('/')


def submitreport(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":


                Student_Name=request.POST['Student_Name']
                Program=request.POST['Program']
                Report_File=request.FILES['report']
                student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
                studentname=Student_Profile.objects.get(User_id=student_signupname.user_id)
            
                data=Student_Submit_Evaluation(Student_Name=Student_Name,Student_Program=Program,Student_id=studentname,Report_File=Report_File,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                
                    
                data.save()
                thank=True
                msg="Successfully Submitted Report"
                return render(request,'student/page-dashboard-student.html',{'thank':thank,'msg':msg})

            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.get(Student_ID=student.StudentId)   
            register=Registration.objects.filter(Student_id=student.StudentId)
            studentname=Student_Profile.objects.filter(StudentId=student.StudentId)
            return render(request,'student/submitreport.html',{'studentname':studentname,'register':register})
            
            

        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')


   

def events(request):
    try:
        if request.session['role']=="Student":
            if request.method=="POST":
                name=request.POST['name']
                department=request.POST['department']
                semester=request.POST['semester']
                course=request.POST['course']
                date=request.POST['date']
                time=request.POST['time']
                coursedata=Course.objects.get(Cid=course)
                tid=coursedata.Instructor_id
                
                data=MeetingAppointment(Course_id=coursedata,Department_id=Department.objects.get(Did=department),Student_ID=Student_Profile.objects.get(StudentId=name),Semester_ID=Semester.objects.get(SamesterId=semester),Date=date,Time=time,uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
                data.save()
                thank=True
                msg="Your Appointment is Proceed"
                return render(request,'student/page-dashboard-student.html',{'thank':thank,'msg':msg})
        
        
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            meeting=MeetingAppointment.objects.filter(Student_ID=student.StudentId).order_by('-Appointment_id')[:]
            return render(request,'student/events.html',{'data':courses,'meeting':meeting})      
        
        
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')

def showevents(request):
    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=MeetingAppointment.objects.get(Appointment_id=uid)
        mydata=SerMeeting(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

def email(request):
    try:
        if request.session['role']=="Student":
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'])
            return render(request,'student/page-dashboard-student.html',{'student_signupname':student_signupname})  
         
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

           
    except:
        return redirect('/')


def submitassignment(request):
    # try:
    if request.session['role']=="Student":
        if request.method=="POST":
            AssignmentId = request.POST['AssignmentId']
            name=request.POST['name']
            roll=request.POST['roll']
            courses=request.POST['courseid']
            Section=request.POST['section']
            assignmentfile=request.FILES['file']
            check = Student_Assigment.objects.filter(AsssigmentId=AssignmentId)
            if check:
                messages.success(request,"Already Uploaded")
                return redirect('/student/assignments')

            data=Student_Assigment(AsssigmentId=AssigmentModel.objects.get(AsssigmentId=AssignmentId),Assigment_File=assignmentfile,roll=roll,section=Section,Student_id=Student_Profile.objects.get(User_id=request.session['userid']),Course_id=Course.objects.get(Cid=courses),uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
            data.save()
            messages.success(request,"Sucessfully Submitted")
            return redirect('/student/assignments')
                
               
    else:
        thank=True
        msg='Your are not a Student'
        return render(request,'index.html',{'thank':thank,'msg':msg})
    
    
    # except:
    #     return redirect('/')

def logout(request):
    
    try:
        if request.session.has_key('role'):
            del request.session['role']
            del request.session['userrole']
            del request.session['username']
            del request.session['userid']
        return redirect('/')
        
        if request.session.has_key("senderid"):
            del request.session['senderid']
            del request.session['sendername']
            del request.session['senderimg']
        return redirect('/')
    
    except:
        return redirect('/')


def videocall(request):
    try:
        if request.session['role']=="Student":
            return render(request,'videocalling/index.html')
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
    
        

def onlineclass(request):
    try:
        if request.session['role']=="Student":
            return redirect('https://solutions.agora.io/education/web/')
            
        else:
            thank=True
            msg='Your are not a Student'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        
    except:
        return redirect('/')


def chat(request):
    try:
        if request.session['role']=="Student":
            return redirect('chat/')
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')

        
def midterm(request):
    
    # try:
    if request.session['role']=="Student":

        if request.method=="POST":
            
            course_id=request.POST['courses']
            data=MidtermModel.objects.filter(Course_id=course_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-MidtermId')[:] 
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            studentname=student.First_name
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            result = urlopen('http://just-the-time.appspot.com/')
            result = result.read().strip()
            result_str = result.decode('utf-8')
            present=result_str[:10]
            present = pd.to_datetime(present).date()
            
            return render(request,'student/midterm.html',{'course':data,'data':courses,'name':studentname,'present':present})
            # return render(request,'student/midterm.html',{'course':data,'data':courses,'name':studentname})

        student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
        student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        studentname=student.First_name
        courses=Student_Course.objects.filter(Student_ID=student.StudentId)
        a=courses.values_list('Courses', flat=True)

           

        data=MidtermModel.objects.filter(Course_id__in=a,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'], Status="True")
        result = urlopen('http://just-the-time.appspot.com/')
        result = result.read().strip()
        result_str = result.decode('utf-8')
        present=result_str[:10]
        present = pd.to_datetime(present).date()
        return render(request,'student/midterm.html',{'data':courses,'name':studentname,'course':data,'present':present})

    #     else:
    #         thank=True
    #         msg='Your are not a Student'
    #         return render(request,'index.html',{'thank':thank,'msg':msg})      
        
    # except:
    #     return redirect('/')

def showmidterm(request):
    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=MidtermModel.objects.get(MidtermId=uid)
        mydata=Ser_Midterm(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

def finalexam(request):
    
    # try:
    if request.session['role']=="Student":

        if request.method=="POST":
            
            course_id=request.POST['courses']
            data=FinalExamModel.objects.filter(Course_id=course_id,uniId__in=request.session['uniid'],branchId__in=request.session['branchid']).order_by('-FinalExamId')[:] 
            student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
            student=Student_Profile.objects.get(User_id=student_signupname.user_id)
            studentname=student.First_name
            courses=Student_Course.objects.filter(Student_ID=student.StudentId)
            result = urlopen('http://just-the-time.appspot.com/')
            result = result.read().strip()
           
            result_str = result.decode('utf-8')
            present=result_str[:10]
            present = pd.to_datetime(present).date()
          
            return render(request,'student/finalexam.html',{'course':data,'data':courses,'name':studentname,'present':present})
            # return render(request,'student/finalexam.html',{'course':data,'data':courses,'name':studentname})

        student_signupname=Student_Signup.objects.get(user_id=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])  
        student=Student_Profile.objects.get(User_id=student_signupname.user_id)
        studentname=student.First_name
        courses=Student_Course.objects.filter(Student_ID=student.StudentId)
        a=courses.values_list('Courses', flat=True)

           

        data=FinalExamModel.objects.filter(Course_id__in=a,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'], Status="True")
        result = urlopen('http://just-the-time.appspot.com/')
        result = result.read().strip()
        result_str = result.decode('utf-8')
       
        present=result_str[:10]
        
        present = pd.to_datetime(present).date()
      
        
        return render(request,'student/finalexam.html',{'data':courses,'name':studentname,'course':data,'present':present})

    #     else:
    #         thank=True
    #         msg='Your are not a Student'
    #         return render(request,'index.html',{'thank':thank,'msg':msg})      
        
    # except:
    #     return redirect('/')

def showfinalexam(request):
    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=FinalExamModel.objects.get(FinalExamId=uid)
        mydata=Ser_FinalExam(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))


def submitmidterm(request):
    # try:
    if request.session['role']=="Student":
        if request.method=="POST":
            MidtermId = request.POST['MidtermId']
            name=request.POST['name']
            roll=request.POST['roll']
            courses=request.POST['courseid']
            Section=request.POST['section']
            assignmentfile=request.FILES['file']
            check = Student_Midterm.objects.filter(MidtermId=MidtermId)
            if check:
                messages.success(request,"Already Uploaded")
                return redirect('/student/midterm')

            data=Student_Midterm(MidtermId=MidtermModel.objects.get(MidtermId=MidtermId),Midterm_File=assignmentfile,roll=roll,section=Section,Student_id=Student_Profile.objects.get(User_id=request.session['userid']),Course_id=Course.objects.get(Cid=courses),uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
            data.save()
            messages.success(request,"Sucessfully Submitted")
            return redirect('/student/midterm')
                
               
    else:
        thank=True
        msg='Your are not a Student'
        return render(request,'index.html',{'thank':thank,'msg':msg})
    
    
    # except:
    #     return redirect('/')



def submitfinalexam(request):
    # try:
    if request.session['role']=="Student":
        if request.method=="POST":
            FinalExamId = request.POST['FinalExamId']
            name=request.POST['name']
            roll=request.POST['roll']
            courses=request.POST['courseid']
            Section=request.POST['section']
            assignmentfile=request.FILES['file']
            check = Student_FinalExam.objects.filter(FinalExamId=FinalExamId)
            if check:
                messages.success(request,"Already Uploaded")
                return redirect('/student/finalexam')

            data=Student_FinalExam(FinalExamId=FinalExamModel.objects.get(FinalExamId=FinalExamId),FinalExam_File=assignmentfile,roll=roll,section=Section,Student_id=Student_Profile.objects.get(User_id=request.session['userid']),Course_id=Course.objects.get(Cid=courses),uniId=UniversityAccount.objects.get(UniId__in=request.session['uniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['branchid']))
            data.save()
            messages.success(request,"Sucessfully Submitted")
            return redirect('/student/finalexam')
                
               
    else:
        thank=True
        msg='Your are not a Student'
        return render(request,'index.html',{'thank':thank,'msg':msg})
    
    
    # except:
    #     return redirect('/')
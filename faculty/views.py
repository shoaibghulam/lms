from django.shortcuts import render,HttpResponse,redirect
from faculty.models import Ser_Exam_result,User_Signup,Materialclass,Course,Instructor,NotificationModel,AssigmentModel,Department,Teacher_syllabus,TeacherApplication,Query_Admin,SerTeacher,User_Stories,CourseVideos,Faculty_Development,Exam_Result,Faculty_Evaluation,Semester,Exam_Result,onlinequiz,MidtermModel,Ser_Midterm,FinalExamModel,Ser_FinalExam,quaizsheet
from student.models import Application,Student_Signup,Student_Course,Student_Profile,Student_Assigment,MeetingAppointment,SerStudent,Ser_Assigment,Ser_App,SerMeeting,Student_Midterm,Ser_Midterms,Student_FinalExam,Ser_FinalExams,Batch,SerStudentCourse
from library.models import Books,BookAuthor
from django.http import HttpResponse
from passlib.hash import pbkdf2_sha256
from django.core.mail import send_mail,EmailMultiAlternatives
from django.core.paginator import Paginator
from administrator.models import AcademicCalendarModel,FacultyCalendarModel,Form,Admin_Notification,role,RoomReservation,Rooms,menu,MenuOrders, menuSer,FacultyAttendence,Faculty_Evaluation_Report,Semester_Schedule,Exam_Schedule,StudentAttendence
import random
import json
from django.db.models import Q
from django.contrib import messages
from django.template import RequestContext
from UniversityApp.models import UniversityAccount,UniversityBranch
from urllib.request import urlopen
import pandas as pd
import datetime
from django.views.decorators.csrf import csrf_exempt

import hashlib
import hmac
import base64
import time
from  zoomus import ZoomClient
import pusher
pusher_client = pusher.Pusher(
  app_id='980079',
  key='088b51ea5617a50f8ad0',
  secret='b2a51edb2c8eebe2aad7',
  cluster='ap2',
  ssl=True
)
# Create your views here.
# zoom meeting api start
client = ZoomClient('tgs2Q91LTDqTwMZneinf0w', 'kfpR6fi0K51zFLR5PaDvICFv2ekOQ9SLTaVl')

# zoom meeting api end
# signatue generate for meeinting start
def generateSignature(data):
    ts = int(round(time.time() * 1000)) - 30000;
    msg = data['apiKey'] + str(data['meetingNumber']) + str(ts) + str(data['role']);    
    message = base64.b64encode(bytes(msg, 'utf-8'));
    # message = message.decode("utf-8");    
    secret = bytes(data['apiSecret'], 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256);
    hash =  base64.b64encode(hash.digest());
    hash = hash.decode("utf-8");
    tmpString = "%s.%s.%s.%s.%s" % (data['apiKey'], str(data['meetingNumber']), str(ts), str(data['role']), hash);
    signature = base64.b64encode(bytes(tmpString, "utf-8"));
    signature = signature.decode("utf-8");
    return signature.rstrip("=");
# signatue generate for meeinting end
def handler404(request,exception):
    return render(request,'page-error.html')

def fdashboard(request):
    try:
        if request.session['role']=="Teacher":
            form=Form.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'],FileCategory="facultyguidline")
            cacform=Form.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'],FileCategory="cacforms")
            instructer_data=User_Signup.objects.get(user_id=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']) 
            
            return render(request,'faculty/page-dashboard.html',{'form':form,'cacform':cacform,'instructer_data':instructer_data})

           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            

    except:
        return redirect('/')


  

#semester form guidline
def formguidline(request):
    try: 
        if request.session['role']=="Teacher":
            appform=Form.objects.filter(FileCategory="applicationform",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            thesisform=Form.objects.filter(FileCategory="thesisguidline",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            placeform=Form.objects.filter(FileCategory="placementforms",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            return render(request,'faculty/formguidline.html',{'appform':appform,'thesisform':thesisform,'placeform':placeform})

        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
         return redirect('/')
#semester library
def library(request):
    # libary html page data
    try:
        if request.session['role']=="Teacher":
            datas= Books.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']).order_by('-BookId')
            paginator = Paginator(datas,3)
            pages=request.GET.get('page',3)
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
                return render(request,'faculty/librarysearch.html',alldata)
        
        
            return render(request,'faculty/library.html',alldata)
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
       return redirect('/faculty/library')
    
#semester library
def digitallibrary(request):
    try:
        if request.session['role']=="Teacher":
            if request.method == "POST":
                BookTitle=request.POST['BookTitle']
                data=Books.objects.filter(Bookcategory="digitallibrary",BookTitle__icontains=BookTitle,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                return render(request,'faculty/digitallibrary.html',{'data':data})
            data= Books.objects.filter(Bookcategory="digitallibrary",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            return render(request,'faculty/digitallibrary.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

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

#semester Phd digital library
def Phddigitallibrary(request):
    try: 
        if request.session['role']=="Teacher":
            if request.method == "POST":
                BookTitle=request.POST['BookTitle']
                data=Books.objects.filter(Bookcategory="digitallibraryphd",BookTitle__icontains=BookTitle,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                return render(request,'faculty/Phddigitallibrary.html',{'data':data})
            data= Books.objects.filter(Bookcategory="digitallibraryphd",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            return render(request,'faculty/Phddigitallibrary.html',{'data':data}) 
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')
    
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
#semester academic calendar
def academiccalendar(request):
    try:
        if request.session['role']=="Teacher":
            data=AcademicCalendarModel.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            return render(request,'faculty/academiccalendar.html',{'data':data}) 
            
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')
    

       

#semester faculty calendar
def facultycalendar(request):
    try:
        if request.session['role']=="Teacher":
            userdata= User_Signup.objects.get(user_id=1)
            id=Instructor.objects.get(username=userdata,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            dep=Department.objects.filter(Instructor_id=id.tid)
            ids=list()
            for getid in dep:
                ids.append(getid.Did)
           
            data=FacultyCalendarModel.objects.filter(Department_id__in=ids)
            return render(request,'faculty/facultycalendar.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
             
    except:
        return redirect('/')

#search examresult
def examresult(request):
    if request.method=="POST":
        semester = request.POST['semester']
        courses = request.POST['courses']
        batch=request.POST['batch']
        request.session['studentbatch']=batch
        request.session['studentsemester']=semester
        courseid=request.POST['courses']
        request.session['course']=courseid
        request.session['batch']=batch
        id=request.session['facultyuserid']
        # batchdata= Batch.objects.
        course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
       
        checking = Exam_Result.objects.filter(InstructerId=course_data,Batch_id=batch,Semester_ID=semester,Course_id=courseid,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
       
        studentlist =list()
        
        for i in checking:
            studentlist.append(i.Student_ID.StudentId)
        
        data=Student_Course.objects.filter(~Q(Student_ID__in = studentlist),Semester_ID=semester,StudenBatch=batch,Courses=courseid,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
        print(data)
        student_courselistId = []
        for k in data:
            student_courselistId.append(k.Student_Course_ID)
        request.session['studentcourseid'] = student_courselistId
        status = False
        if data:
            status = True
        department = ''
        if data:
            department = data[0].Department_id.Did
     
        
        
        batchdata = Batch.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
        courses=Course.objects.filter(Instructor_id=course_data.tid)
        semester = Semester.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
        return render(request,'faculty/examresult.html',{'status':status,'semester':semester,'batch':batchdata,'data':data,'courses':courses,'department':department,'course':courseid})

    id=request.session['facultyuserid']
    course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    batch = Batch.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    courses=Course.objects.filter(Instructor_id=course_data.tid)
    semester = Semester.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    return render(request,'faculty/examresult.html',{'courses':courses,'batch':batch,'semester':semester})
    

   
         

#ADD all STUDENT RESULT

def resultentry(request):
    if request.method=="POST":
        project=request.POST.getlist('project')
        assignment=request.POST.getlist('q/a')
        midterm=request.POST.getlist('midterm')
        final=request.POST.getlist('final')
        total=request.POST.getlist('total')
        course=request.POST['course']
        dep=request.POST['depart']
        obtain = request.POST.getlist('Obtained_marks')
        grade = request.POST.getlist('Grade')
        sid=request.POST.getlist('sid')
        cid=Course.objects.get(Cid=course)
        studentbatch=request.session['studentbatch']
        studentsemester=request.session['studentsemester']
        length_of_list = len(project)
     
     
        Instructorid=Instructor.objects.get(username=request.session['facultyuserid'])
        
        for i in range(length_of_list):
            data=Exam_Result(Batch_id=Batch.objects.get(Batch_id=studentbatch),Semester_ID=Semester.objects.get(SamesterId=studentsemester),Grade = grade[i] ,Obtained_marks=obtain[i],Course_id=cid,
            Project_Marks=project[i],Quiz_Assignment_Marks=assignment[i],
            Midterm_Marks=midterm[i],Final_Marks=final[i],Total_Marks=total[i]
            ,InstructerId=Instructorid,Department_id=Department.objects.get(Did=dep),
            Student_ID=Student_Profile.objects.get(StudentId=sid[i]),
            uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid'])
            ,branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
            data.save()
        
        id=request.session['facultyuserid']
        course_data=Instructor.objects.get(username=id)
        courses=Course.objects.filter(Instructor_id=course_data.tid)
        batch = Batch.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
        messages.success(request,"Sucessfully Uploaded All the Students Marks")
        return redirect('/faculty/examresult')
        



  

# Edit Exam Result Search

def editexamresult(request):
    if request.method == "POST":
        semester=request.POST['semester']
        batch=request.POST['batch']
        courses=request.POST['courses']
        request.session['lockcourse'] = courses
        request.session['lockbatch'] = batch
        request.session['locksemester'] = semester
        Instructorid=Instructor.objects.get(username=request.session['facultyuserid'])
        data = Exam_Result.objects.filter(Batch_id=batch,Semester_ID=semester,InstructerId = Instructorid.tid,Course_id=courses)
        status = False
        if data:
            if data[0].Status == "lock":
                status = True
          

        
        courses=Course.objects.filter(Instructor_id=Instructorid.tid)
        batch = Batch.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
        semester = Semester.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])

        return render(request,'faculty/editexamresult.html',{'status':status,'courses':courses,'data':data,'batch':batch,'semester':semester})
        

    id=request.session['facultyuserid']
    course_data=Instructor.objects.get(username=id)
    courses=Course.objects.filter(Instructor_id=course_data.tid)
    batch = Batch.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    semester = Semester.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    status = False
    return render(request,'faculty/editexamresult.html',{'status':status,'courses':courses,'batch':batch,'semester':semester})
        

#lock Result 

  
def lockresult(request):
    BatchId = request.session['lockbatch']
    CourseID = request.session['lockcourse']
    SemesterId = request.session['locksemester']
    TeacherID=request.session['facultyuserid']
    teacherProfile=Instructor.objects.get(username=TeacherID)
    data = Exam_Result.objects.filter(Batch_id=BatchId,Semester_ID=SemesterId ,Course_id=CourseID,InstructerId=teacherProfile.tid)
    for i in data:
        i.Status = "lock"
        i.save()
    messages.success(request,"Lock Result Sucessfully")
    del request.session['lockbatch']
    del request.session['lockcourse']
    del request.session['locksemester']
    return redirect('/faculty/editexamresult')

#show student marks and edit individual

def ShowStudentMarks(request):
    if request.method == "POST":
        ExamResultId = request.POST['ExamstudentId']
        Project = request.POST['pmarks']
        Quiz = request.POST['qmarks']
        Mid = request.POST['mmarks']
        Final = request.POST['fmarks']
        data = Exam_Result.objects.get(Exam_Result_id=ExamResultId)
        data.Project_Marks = Project
        data.Quiz_Assignment_Marks = Quiz
        data.Midterm_Marks = Mid
        data.Final_Marks = Final
        Student_Total_marks = int(Project)+int(Quiz)+int(Mid)+int(Final)
        data.Obtained_marks = Student_Total_marks
        
        if Student_Total_marks < 60:
            data.Grade = 'F'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')
        elif Student_Total_marks >=60 and Student_Total_marks <= 66:
            data.Grade = 'C'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')

        elif Student_Total_marks >=67 and Student_Total_marks <= 73:
            data.Grade = 'C+'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')

        elif Student_Total_marks >=74 and Student_Total_marks <= 80:
            data.Grade = 'B'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')


        elif Student_Total_marks >=81 and Student_Total_marks <= 87:
            data.Grade = 'B+'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')


        elif Student_Total_marks >=88 and Student_Total_marks <= 100:
            data.Grade = 'A'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')

        else:
            data.Grade = 'F'
            data.save()
            messages.success(request,"Update Sucessfully")
            return redirect('/faculty/editexamresult')






        


     

    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Exam_Result.objects.get(Exam_Result_id=uid)
        mydata=Ser_Exam_result(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))
   

#Individual Upload Exam Marks

def IndividualMarksUpload(request):
    if request.method == "POST":
        Project = request.POST['pmarks']
        Quiz = request.POST['qmarks']
        Mid = request.POST['mmarks']
        Final = request.POST['fmarks']
        Total = request.POST['tmarks']
        studentId = request.POST['studentId']
        course=request.session['course']
        dep=request.session['depart']
        obtain = request.POST['SObtained_marks']
        grade = request.POST['SGrade']
        cid=Course.objects.get(Cid=course)
        Instructorid=Instructor.objects.get(username=request.session['facultyuserid'])
        studentbatch=request.session['studentbatch']
        studentsemester=request.session['studentsemester']
        data=Exam_Result(Grade = grade ,Obtained_marks=obtain,Batch_id=Batch.objects.get(Batch_id=studentbatch),Semester_ID=Semester.objects.get(SamesterId=studentsemester),Course_id=cid,Project_Marks=Project,Quiz_Assignment_Marks=Quiz,Midterm_Marks=Mid,Final_Marks=Final,Total_Marks=Total,InstructerId=Instructorid,Department_id=Department.objects.get(Did=dep),Student_ID=Student_Profile.objects.get(StudentId=studentId),uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
        data.save()
        messages.success(request,"Upload Marks Sucessfully")
        return redirect('/faculty/examresult')



    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Student_Profile.objects.get(StudentId=uid)
        mydata=SerStudent(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

#semester userstories
def facultyform(request):
    
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                checkboxlist=list()
                name=request.POST['name']
                depart=request.POST['department']
                courses=request.POST['courses']
                degree=request.POST['Degress']
                experties=request.POST['expertise']
                corearea=request.POST['corearea']
                ratio=request.POST['ratio']
                Area=request.POST['Area']
                id=request.session['facultyuserid']
                checkbox=request.POST.getlist('checkbox1')
                course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                tid=course_data.tid
                checkboxlist.append(checkbox)
                data=Faculty_Development(Name=name,Highest_Degree=degree,Department=depart,Subject=courses,Course_you_Teach=experties,Core_Area_to_you_would_like_to_develop=corearea,Teacher_Research_Ratio=ratio,particular_area_of_work=Area,Instructor_id=Instructor.objects.get(username=id),area_of_expertise=checkboxlist,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Form Successfully Submitted")
                return redirect('/faculty/facultyform')
              

            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            depart=Department.objects.filter(Instructor_id=course_data.tid)
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            teacher_name=course_data.First_Name
            return render(request,'faculty/facultyform.html',{'depart':depart,'courses':courses,'course_data':teacher_name}) 
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')
        

#semester coursefile
def coursefile(request):
    try:
        if request.session['role']=="Teacher":
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/coursefile.html',{'data':courses})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
           
    except:
        return redirect('/')
       


     

#semester roomreservation
def roomreservation(request):
    try:
        if request.session['role']=="Teacher":
            data= Rooms.objects.filter(RoomStatus="Available",uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            alldata={
                'data':data
            }
            return render(request,'faculty/roomreservation.html',alldata) 
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

        

#semester foodreservation
def foodreservation(request):
    try:
    
        if request.session['role']=="Teacher":
            data= menu.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            alldata={
                'data':data
            }
            return render(request,'faculty/foodreservation.html',alldata) 
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    
    except:
        return redirect('/')



#semester dashboard
def fvledashboard(request):
    try:
        if request.session['role']=="Teacher":
            return render(request,'faculty/fvledashboard.html') 
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

        



#semester myclass
def myclass(request):
    try:
        if request.session['role']=="Teacher":
            return render(request,'faculty/myclass.html') 
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

         

def classmaterial(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":

                title=request.POST['title']
                category=request.POST['category']
                course=Course.objects.get(Cid=request.POST['course']) 
                File=request.FILES['file']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                
                data3=Materialclass(Title=title,Category=category,MaterailFile=File,Course_id=course,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data3.save()
                id=request.session['facultyuserid']
                course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
                courses=Course.objects.filter(Instructor_id=course_data.tid)
                messages.success(request,"Lecture Slides Uploaded")
                return render(request,'faculty/classmaterial.html',{'data':courses})

                
                
            
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/classmaterial.html',{'data':courses})
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
    except:
        return redirect('/')



#Online Lecture 
def onlinelecture(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            material=Materialclass.objects.filter(Instructor_id=course_data.tid,Category="lectures")
            return render(request,'faculty/onlinelecture.html',{'material':material})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')
    

#OnlineBook
def onlinebook(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            material=Materialclass.objects.filter(Instructor_id=course_data.tid,Category="ebooks")
            return render(request,'faculty/onlinebook.html',{'material':material})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')
    

#Onlinequiz
def Onlinequiz(request):
   

    try:

        if request.session['role']=="Teacher":
            if request.method=="POST":

                coursename=request.POST['category']
                marks=request.POST['marks']
                department=request.POST['department']
                semester=request.POST['semester']
                semesterdata=Semester.objects.get(Samester_Name=semester,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                semestername=semesterdata.SamesterId
                Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                title=request.POST['title']
                data=onlinequiz(semester=semester,quizlink=marks,Course_id=Course.objects.get(Cid=coursename),Instructor_id=Instructor.objects.get(username=request.session['facultyuserid']),Department_id=Department.objects.get(Department_name=department),Title=title,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request, 'Quiz Successfully Added')
                courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
                data=onlinequiz.objects.filter(Instructor_id=Instructor_id.tid)
                return render(request,'faculty/onlinequiz.html',{'courses':courses,'data':data})
               
                    

            Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
            data=onlinequiz.objects.filter(Instructor_id=Instructor_id.tid)
            return render(request,'faculty/onlinequiz.html',{'courses':courses,'data':data})

        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')

def deletequiz(request,id):
    try:
        if request.session['role']=="Teacher":
            data=onlinequiz.objects.get(onlinequizid=id)
            data.delete()
            Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
            data=onlinequiz.objects.filter(Instructor_id=Instructor_id.tid)
            messages.error(request,"Delete Quiz Successfully")
            # return render(request,'faculty/onlinequiz.html',{'courses':courses,'data':data})
            return redirect('/faculty/onlinequiz')
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')


# Active or disable quiz
def quizstatus(request, id, status):
    Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    data=onlinequiz.objects.get(pk=id,Instructor_id=Instructor_id.tid)
    status = status
    msg=""
    if status =="active":
        data.status="disable"
        msg="Quiz is Disabled"
    elif status=="disable" :
        data.status="active"
        msg="Quiz is Active"
    data.save()
    messages.success(request,msg)
    return redirect('/faculty/onlinequiz')
    





#mygrade
def mygrade(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/mygrade.html',{'course':courses})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        
    
    except:
        return redirect('/')



#notification    
def notification(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['title']
                notifycategory=request.POST['notify']
                category=Course.objects.get(Cid=request.POST['category'])
                description=request.POST['description']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data3=NotificationModel(NotificationTitle=title,Category=notifycategory,NotificationDesc=description,Course_id=category,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data3.save()
                messages.success(request,"Add Notification Sucessfully")
                return redirect('/faculty/notification')

            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            notification=NotificationModel.objects.filter(Instructor_id=course_data.tid)
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/mynotification.html',{'courses':courses,'notification':notification})
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
    except:
        return redirect('/')
        

#createnotification
def createnotification(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            notification=NotificationModel.objects.filter(Instructor_id=course_data.tid,Category="Section")
            return render(request,'faculty/createnotification.html',{'notification':notification})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
         return redirect('/')
    



#Application
def application(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['title']
                message=request.POST['message']
                img=request.FILES['file']
                id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=TeacherApplication(ApplicationTitle=title,ApplicationMessage=message,ApplicationAttachment=img,Instructor_id=id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.error(request,"Application Add Sucessfully")
                return redirect('/faculty/application')

            data=TeacherApplication.objects.filter(Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']))
            return render(request,'faculty/application.html',{'data':data})    
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
         return redirect('/')
    


#Create Application
def createapplication(request):
    try:
        if request.session['role']=="Teacher":
            return render(request,'faculty/createapplication.html')
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
    
        


 
 
#create createprogramnotification
def createprogramnoti(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            notification=NotificationModel.objects.filter(Instructor_id=course_data.tid,Category="program")
            return render(request,'faculty/createprogramnoti.html',{'notification':notification})
   
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')

#create student application
def app(request):
    try:
        if request.session['role']=="Teacher":
            id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            data=Application.objects.filter(Instructor_id=id)
            return render(request,'faculty/app.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
         return redirect('/')

def showstudentapp(request):
    if request.method == 'POST':
        Techer_Reply=request.POST['Techer_Reply']
        id = request.POST['sid']
        
        data=Application.objects.get(ApplicationId=id)
        data.Techer_Reply=Techer_Reply
        data.save()
        messages.success(request,"Reply Successfully")
        return redirect('/faculty/app')


        

    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Application.objects.get(ApplicationId=uid)
        mydata=Ser_App(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

###############Shoaib khan##########################   
def signup(request):
    if request.method=="POST":
        try:
        
            username=request.POST['username']
            email=request.POST['email']
            checkbox1=request.POST.get('checkbox1','off')
            checkbox2=request.POST.get('checkbox2','off')
            password=request.POST['password1']
            password1=request.POST['password2']
            if password!=password1:
                thank=True
                msg="The Two Password Fields Doesnot Match"
                return render(request,'index.html',{'msg':msg,'thank':thank})

            if checkbox1=="on" and checkbox2=="on":
                thank=True
                msg="Please Select Only One"
                return render(request,'index.html',{'msg':msg,'thank':thank})
            elif checkbox1=="off" and checkbox2=="off":
                thank=True
                msg="Please Select Atleast One Teacher or Student"
                return render(request,'index.html',{'msg':msg,'thank':thank})
            elif checkbox1=="on":
                password_encrpt=pbkdf2_sha256.hash(password)
                checkuser_name = User_Signup.objects.filter(username=username)
                checkuser_email = User_Signup.objects.filter(email=email)
                if checkuser_name or checkuser_email:
                    thank=True
                    msg="The username or email is already"
                    return render(request,'index.html',{'msg':msg,'thank':thank})
                    
                data=User_Signup(username=username,email=email,password=password_encrpt)
                data.save()
                thank=True
                msg="Signup Sucessfully"
                return render(request,'index.html',{'msg':msg,'thank':thank})
            elif checkbox2=="on":
                password_encrpt=pbkdf2_sha256.hash(password)
                checkuser_name = Student_Signup.objects.filter(username=username)
                checkuser_email =Student_Signup.objects.filter(email=email)
                if checkuser_name or checkuser_email:
                    thank=True
                    msg="The username or email is already"
                    return render(request,'index.html',{'msg':msg,'thank':thank})
                    
                data=Student_Signup(username=username,email=email,password=password_encrpt)
                data.save()
                thank=True
                msg="Signup Sucessfully"
                return render(request,'index.html',{'msg':msg,'thank':thank})
        
        except:
            return redirect('/')

  
def login(request):
    if request.method=="POST":
        checkbox=request.POST.get('checkbox','off')
        email=request.POST['email']
        password=request.POST['password']
        if checkbox=="on":
            try:
                data=User_Signup.objects.get(email=email)
                try:
                    image=Instructor.objects.get(tid=data.user_id)
                    request.session['senderimg']=str(image.img)
                except:
                    None
              
    
                if data:
                    encrpt=data.password
                    role=data.role
                    encrpt=pbkdf2_sha256.verify(password,encrpt)
                if encrpt and role=="null":
                    data=User_Signup.objects.get(email=email)
                    request.session['username'] = data.username
                    request.session['userid'] = data.user_id
                    request.session['role'] = data.role
                    request.session['userrole'] = data.role
                    thank=True
                    msg="Successfully Login"
                    return render(request,'index.html',{'thank':thank,'msg':msg})
                elif encrpt:

                    data=User_Signup.objects.get(email=email)
                    request.session['username'] = data.username
                    request.session['userid'] = data.user_id
                    request.session['userrole'] = data.role
                   

                    request.session['role'] = data.role
                   
                    return redirect('/faculty/')
                

                else:
                    thank=True
                    msg="Password Incorrect"
                    return render(request,'index.html',{'thank':thank,'msg':msg})
                
                
            except:
                thank=True
                msg="Email Doesnot Exist"
                return render(request,'index.html',{'thank':thank,'msg':msg})
        else:
            try:
                data=Student_Signup.objects.get(email=email)
                try:
                    image=Student_Profile.objects.get(User_id=data.user_id)
                    request.session['senderimg']=str(image.Profile)
                except:
                    None
               
                
                # k=list()
                # for i in image:
                #     k.append(i.Profile)
                # ab=json.dumps(str(k))
        
                # request.session['senderimg']=k
                # return HttpResponse(ab)
               
            
                if data:
                    encrpt=data.password
                    role=data.role
                    encrpt=pbkdf2_sha256.verify(password,encrpt)
                if encrpt and role=="null":
                    data=Student_Signup.objects.get(email=email)
                    request.session['username'] = data.username
                    request.session['userid'] = data.user_id
                    request.session['userrole'] = data.role
                    request.session['role'] = data.role
                    thank=True
                    msg="Successfully Login"
                    return render(request,'index.html',{'thank':thank,'msg':msg})
                if encrpt:
                    data=Student_Signup.objects.get(email=email)
                    request.session['username'] = data.username
                    request.session['userid'] = data.user_id
                    request.session['userrole'] = data.role
                    request.session['role'] = data.role
                                         
                    return redirect('/student/')              
               

                else:
                    thank=True
                    msg="Password Incorrect"
                    return render(request,'index.html',{'thank':thank,'msg':msg})
                
                
            except Student_Signup.DoesNotExist:
                thank=True
                msg="Email Doesnot Exist"
                return render(request,'index.html',{'thank':thank,'msg':msg})

            
            


# verification 
def verification(request,verification,username):
    try:
        if request.session['role']=="Teacher":
            data= User_Signup.objects.get(username=username)
        
            if data.token==verification:
                updata= User_Signup.objects.get(username=username)
                updata.verify='verified'
                updata.save()
                return redirect('/login')

        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        

    except:
        return redirect('/')


def forgetrequest(request):
    try:
        if request.session['role']=="Teacher":
    
            email=request.GET.get('email')
        
            token=random.randint(1000,100000)
        
            data=User_Signup.objects.get(email=email)
            username=data.username
            data.token=token
            data.save()

            subject, from_email, to = 'Forget Password', 'no-replay@gwadarengineeringworks.com', email
            html_content = f'''
                    <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Finish creating your account</h1>
                        <p> 
                Your email address has been registered with lms. To validate your account and activate your ability to send email campaigns, please complete your profile by clicking the link below:</p>
                    <div style='width:300px; margin:0 auto;'> <a href='http://127.0.0.1:8000/forget/{token}/{username}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
                </div>
                    '''
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse('sent')
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    
    except:
        return redirect('/')


def forget(request,verification,username):
    try:
        if request.session['role']=="Teacher":
            token=verification
            username=username
            return render(request,'forget.html',{'token':token,'username':username})
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})


    except:
        return redirect('/')


def logout(request):
    try:
    
   
        if request.session.has_key('role'):
            del request.session['role']
            # del request.session['userrole']
            del request.session['facultyusername']
            del request.session['facultyuserid']
            del request.session['senderimg']
        return redirect('/')
        if request.session.has_key("senderid"):
            del request.session['senderid']
            del request.session['sendername']
            del request.session['senderimg']
        return redirect('/')
    
    except:
        return redirect('/')

#Assignment
def assignment(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['title']   
                desct=request.POST['desct']
                startdate = request.POST['startdate']
                enddate = request.POST['enddate']   
                coursename=Course.objects.get(Cid=request.POST['category'])  
                mfile=request.FILES['mfile']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=AssigmentModel(StartDate=startdate,EndDate=enddate,AssigmentTitle=title,AssigmentDesc=desct,AssigmentFile=mfile,Course_id=coursename,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Assignment Uploaded Successfully")
                return redirect('/faculty/assignment')
              
           

            
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            assignment=AssigmentModel.objects.filter(Instructor_id=course_data.tid).order_by('-AsssigmentId')
            return render(request,'faculty/assignments.html',{'courses':courses,'assignment':assignment})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')

#create creategradebookon
def creategradebook(request):
    if request.method=="POST":
        coursename=request.POST['category']
        MidMarks=request.POST['Mid_Marks']
        total_marks=request.POST['Total_Marks']
        Obtain_Marks=request.POST['Obtain_Marks']
        coursedata = Course.objects.get(Cid=coursename)
        coursedata.Total_Marks=total_marks
        coursedata.Obtain_Marks=Obtain_Marks
        coursedata.MidTerm_Marks=MidMarks
        coursedata.save()
        messages.success(request,"Edit Sucessfully")
        return redirect('/faculty/creategradebook')

                
                
         

    Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
    courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
    return render(request,'faculty/creategradebook.html',{'courses':courses})
    # try:
    #     if request.session['role']=="Teacher":
    #         if request.method=="POST":
    #             coursename=request.POST['category']
    #             MidMarks=request.POST['Mid_Marks']
    #             total_marks=request.POST['Total_Marks']
    #             Obtain_Marks=request.POST['Obtain_Marks']
    #             coursedata = Course.objects.get(Cid=coursename)
    #             coursedata.Total_Marks=total_marks
    #             coursedata.Obtain_Marks=Obtain_Marks
    #             coursedata.MidTerm_Marks=MidMarks
    #             coursedata.save()
    #             messages.success(request,"Edit Sucessfully")
    #             return redirect('/faculty/creategradebook')

                
                
         

    #         Instructor_id=Instructor.objects.get(username=request.session['userid'],uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
    #         courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
    #         return render(request,'faculty/creategradebook.html',{'courses':courses})

    # except:
    #     return redirect('/')
    
   
def classnotification(request):

    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            notification=NotificationModel.objects.filter(Instructor_id=course_data.tid,Category="class")
            return render(request,'faculty/classnotification.html',{'notification':notification})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')


#syllabus
def syllabus(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            syllabus=Teacher_syllabus.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/syllabus.html',{'syllabus':syllabus})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')


    

#Create syllabus
def createsyllabus(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['semester']
                coursename=request.POST['category']
                department=request.POST['department']
                img=request.FILES['file']
                data=Teacher_syllabus(semester=title,outline=img,Course_id=Course.objects.get(Cid=coursename),Department_id=Department.objects.get(Did=department),Instructor_id=Instructor.objects.get(username=request.session['facultyuserid']),uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Add Syllabus Sucessfully")
                return redirect('/faculty/syllabus')
              
                
            semester=Semester.objects.filter(uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            Instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            courses=Course.objects.filter(Instructor_id=Instructor_id.tid)
            department=Department.objects.filter(Instructor_id=Instructor_id.tid)
            return render(request,'faculty/createsyllabus.html',{'courses':courses,'department':department,'semester':semester})
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})



  
            
    except:
        return redirect('/')
    

    


#semester myclass
def onlinequery(request):
    try:
        if request.session['role']=="Teacher":
            course_data=Instructor.objects.get(username=request.session['facultyuserid'])   
            query=Query_Admin.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/onlinequery.html',{'query':query}) 
         
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
           
    except:
        return redirect('/')



        



def createquery(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                querytitle=request.POST['querytitle']
                querymessage=request.POST['querymessage']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'])
                data=Query_Admin(querytitle=querytitle,querymessage=querymessage,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                thank=True
                messages.error(request,"Query Send Successfully")
                return redirect('/faculty/onlinequery')
        
            return render(request,'faculty/createquery.html')
    
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')      
   
def myroles(request):
    try:
        if request.session['role']=="Teacher":
            id=Instructor.objects.get(username=request.session['facultyuserid'])
            data=role.objects.filter(Instructor_id=id)
            return render(request,'faculty/myroles.html',{'data':data})
           
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
          
    except:
        return redirect('/')   
    
#semester userstories
def userstories(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                I_want_to=request.POST['I_want_to']
                So_that_I_can=request.POST['So_that_I_can']
                category=request.POST['category']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=User_Stories(I_want_to=I_want_to,Category=category,So_that_I_can=So_that_I_can,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Add Story Sucessfully")
                return redirect('/faculty/userstories')
            
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=User_Stories.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/userstories.html',{'data':courses})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')   

 #semester facultyattendance
def facultyattendance(request):
    try:
        if request.session['role']=="Teacher":
    
            if request.method=="POST":
                Month=request.POST['Month']
                Year=request.POST['Year']
                id=request.session['facultyuserid']
                course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
                courses=FacultyAttendence.objects.filter(Instructor_id=course_data.tid,FacultyAttendenceYear=Year,FacultyAttendenceMonth=Month)
                yearMonth = FacultyAttendence.objects.filter(Instructor_id=course_data.tid)
                return render(request,'faculty/facultyattendance.html',{'data':courses,'yearMonth':yearMonth})


            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=FacultyAttendence.objects.filter(Instructor_id=course_data.tid)
            yearMonth = FacultyAttendence.objects.filter(Instructor_id=course_data.tid)
            return render(request,'faculty/facultyattendance.html',{'data':courses,'yearMonth':yearMonth})
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')  




#semester facultyevaluation
def facultyevaluation(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                Report=Faculty_Evaluation_Report.objects.get(Faculty_Evaluation_Report_ID=request.POST['report'])
                reportname=Report.Report_Name
                file=Report.Report_File
                department=Department.objects.get(Did=request.POST['depart'])
                course=Course.objects.get(Cid=request.POST['course']) 
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data3=Faculty_Evaluation(Report_Name=reportname,Department_id=department,Course_id=course,InstructerId=instructor_id,Report_File=file,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data3.save()
                messages.success(request,"Added Sucessfully")
                return redirect('/faculty/facultyevaluation')
                    

            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            depart=Department.objects.filter(Instructor_id=course_data.tid)
            departId = []
            for i in courses:
                departId.append(i.Department_id)
            report=Faculty_Evaluation_Report.objects.filter(Department_id__in=departId)
            return render(request,'faculty/facultyevaluation.html',{'data':courses,'depart':depart,'report':report})
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')  



#semester schedule page
def semesterschedule(request):
        
    try:
        if request.session['role']=="Teacher":
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']) 
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            a=[]
            for i in courses:
                a.append(i.Department_id)
            data=Semester_Schedule.objects.filter(Department_id__in=a)
            return render(request,'faculty/semesterschedule.html',{'data':data})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        
    except:
        return redirect('/') 



def examschedule(request):
    try:
        if request.session['role']=="Teacher":
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']) 
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            a=[]
            for i in courses:
                a.append(i.Department_id)
            data=Exam_Schedule.objects.filter(Department_id__in=a)
            return render(request,'faculty/examschedule.html',{'data':data}) 
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
             
    except:
        return redirect('/')


#semester attendancet

def attendance(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                courses=request.POST['courses']
                year=request.POST['year']
                month=request.POST['month']
                instructer_data=Instructor.objects.get(username=request.session['facultyuserid'])  
                course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
                Instructor_courseid=list()
                for x in course_data:
                    Instructor_courseid.append(x.Cid)
                data=StudentAttendence.objects.filter(Course_id=courses,StudentAttendenceYear=year,StudentAttendenceMonth=month)
                data2=StudentAttendence.objects.filter(Course_id__in=Instructor_courseid)
                return render(request,'faculty/attendance.html',{'course_data':course_data,'data':data,'data2':data2})
            
            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'])  
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            Instructor_courseid=list()
            for x in course_data:
                Instructor_courseid.append(x.Cid)
            data=StudentAttendence.objects.filter(Course_id__in=Instructor_courseid)
            data2=StudentAttendence.objects.filter(Course_id__in=Instructor_courseid)
            return render(request,'faculty/attendance.html',{'course_data':course_data,'data':data,'data2':data2})



        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

   


        

def email(request):
    try:
        if request.session['role']=="Teacher":
            instructer_data=User_Signup.objects.get(user_id=request.session['facultyuserid']) 
            return render(request,'faculty/page-dashboard.html',{'instructer_data':instructer_data})  
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')
 
def studentassignment(request):
    # try:
    if request.session['role']=="Teacher":
        if request.method=="POST":
            courseid=request.POST['courses']
            topic=request.POST['topic']
            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'])  
            data=AssigmentModel.objects.filter(Course_id=courseid,AsssigmentId=topic,Instructor_id=instructer_data.tid)
            AssignmentList = []
            for i in data:
                AssignmentList.append(i.AsssigmentId)
            
            studentlist = Student_Assigment.objects.filter(AsssigmentId__in=AssignmentList)
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            title=AssigmentModel.objects.filter(Instructor_id=instructer_data.tid)
            return render(request,'faculty/studentassignments.html',{'course':course_data,'studentlist':studentlist,'title':title})

            
        instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
        course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
        Instructor_courseid=list()
        for x in course_data:
            Instructor_courseid.append(x.Cid)
        data=Student_Assigment.objects.filter(Course_id__in=Instructor_courseid).order_by('-Student_Assigment_Id')
        title=AssigmentModel.objects.filter(Instructor_id=instructer_data.tid)
        return render(request,'faculty/studentassignments.html',{'course':course_data,'data':data,'title':title})

    #     else:
    #         thank=True
    #         msg='Your are not a Teacher'
    #         return render(request,'index.html',{'thank':thank,'msg':msg})

    # except:
    #     return redirect('/')
        
        
#show student assignment

def showstudentassignment(request):
    if request.method == 'POST':
        marks=request.POST['marks']
        id = request.POST['sid']
        data=Student_Assigment.objects.get(Student_Assigment_Id=id)
        Assignment_file = request.FILES.get('file',False)
        if Assignment_file:
            data.Teacher_Upload=Assignment_file
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentassignment')


        else:
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentassignment')


    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Student_Assigment.objects.get(Student_Assigment_Id=uid)
        mydata=Ser_Assigment(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

def videocall(request):
    try:
        if request.session['role']=="null":
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        else:
            return render(request,'videocalling/index.html')
    except:
        return redirect('/')


def Appointment(request):
    try:
        if request.session['role']=="Teacher":
            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            Instructor_courseid=list()
            for x in course_data:
                Instructor_courseid.append(x.Cid)
            data=MeetingAppointment.objects.filter(Course_id__in=Instructor_courseid,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid']).order_by('-Appointment_id')[:]
            return render(request,'faculty/Appointment.html',{'data':data})


        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

def ShowAppointment(request):
    if request.method == 'POST':
        Techer_Reply=request.POST['Techer_Reply']
        id = request.POST['sid']
        
        data=MeetingAppointment.objects.get(Appointment_id=id)
        data.Techer_Reply=Techer_Reply
        data.save()
        messages.success(request,"Reply Successfully")
        return redirect('/faculty/Appointment')


        

    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=MeetingAppointment.objects.get(Appointment_id=uid)
        mydata=SerMeeting(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))


def chat(request):
    try:
    
        if request.session['role']=="null":
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
        else:
            return redirect('chat/')
    

    except:
        return redirect('/')


def onlineclass(request):
    try:
        if request.session['role']=="Teacher":
            return redirect('https://solutions.agora.io/education/web/')
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    except:
        return redirect('/')

        

###################End Shoaib khan################################

####################shakeeb#######################################
def becometeacher(request):
 
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                img=request.FILES['image']
                firstname=request.POST['firstname']
                lastname=request.POST['lastname']
                gender=request.POST['gender']
                address=request.POST['address']
                phone=request.POST['phone']
                birth=request.POST['birth']
                username=request.session['facultyusername']
                user=User_Signup.objects.get(user_id=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=Instructor(First_Name=firstname,Last_Name=lastname,Gender=gender,Address=address,Phone_Number=phone,Dob=birth,img=img,username=user)
                data.save()
                user.role="Teacher"
                user.save()
                images=Instructor.objects.get(username=request.session['facultyuserid'])
                request.session['senderimg']= str(images.img)
                thank=True
                msg="Your Profile Sucessfully Created"
                return redirect('/faculty/')
            
    
            data=Instructor.objects.filter(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            if data:
                Thank=True
                return render(request,'faculty/becomeinstructor.html',{'thank':Thank})
                
            else:
                return render(request,'faculty/becomeinstructor.html')
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})   
    except:
        return redirect('/')

 

    
def showteacher(request):
    try:
        if request.session['role']=="Teacher":
            userdata = list()
            data=Instructor.objects.filter(username=User_Signup.objects.get(username=request.session['facultyusername']))
            if data:
                for x in data:
                    datas=SerTeacher(x)
                    userdata.append(datas.data)
                return HttpResponse(json.dumps(userdata))
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    except:
        return redirect('/')

def editinstructor(request):
    
        if request.method=="POST":
            username=User_Signup.objects.get(username=request.session['facultyusername'])
            
            data=Instructor.objects.get(username=username,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            data.First_Name=First_Name=request.POST['firstname']
            data.Last_Name=request.POST['lastname']
            data.Gender=request.POST['gender']
            data.Phone_Number=request.POST['phone']
            data.Address=request.POST['address']
            data.Dob=request.POST['birth']
            image=request.FILES.get('image',False)
            if image:
                data.img=request.FILES['image']
          
            data.save()
            request.session['senderimg']= str(data.img)  
            return HttpResponse("Profile has been Update")
    # except:
    #     return HttpResponse(request.session['facultyusername'])

def AddVideos(request):
    try:
        if request.session['role']=="Teacher":
            if request.method =='POST':
                title= request.POST['title']
                description= request.POST['description']
                course=request.POST['course']
                videofile= request.FILES['video']
                id=request.session['facultyuserid']
                teacherdata=Instructor.objects.get(username=id,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
                courses=Course.objects.get(Cid=course)
                data=CourseVideos(VideoTitle=title,VideoDesc=description,VideoFile=videofile,CourseId=courses,InstructerId=teacherdata,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                return HttpResponse("Video uploaded successfully")
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/')


def showvideo(request):
    try:
        if request.session['role']=="Teacher":
            id=request.session['facultyuserid']
            course_data=Instructor.objects.get(username=id)   
            video=CourseVideos.objects.filter(InstructerId=course_data.tid)
            return render(request,'faculty/showvideo.html',{'video':video})
          
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
            
    
    except:
        return redirect('/') 

###################End Shakeeeb################################


###################Baloch################################



#create liststudent
def liststudent(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
                course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
                courses=request.POST['courses']
                data=Student_Course.objects.filter(Courses=courses).distinct()
                return render(request,'faculty/liststudent.html',{'data':data,'course_data':course_data})

            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            Instructor_courseid=list()
            for x in course_data:
                Instructor_courseid.append(x.Cid)
            data=Student_Course.objects.filter(Courses__in=Instructor_courseid).distinct()
            return render(request,'faculty/liststudent.html',{'data':data,'course_data':course_data})
        
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/') 


    



  

def RoomReservationinsert(request):
    try:
        if request.session['role']=="Teacher":
            if request.method =="POST":
                roomid = Rooms.objects.get(RoomId= request.POST['roomid'])
                Participants = request.POST['Participants']
                starttime = request.POST['starttime']
                Endtime = request.POST['Endtime']
                Comments = request.POST['Comments']
                Date = request.POST['date']
                data=RoomReservation(ReservationParticipants=Participants,ReservationComments=Comments,ReservationStartDate=Date,ReservationStartTime=starttime,ReservationEndTime=Endtime,RoomId=roomid,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                bookdata=Rooms.objects.get(RoomId= request.POST['roomid'])
                bookdata.RoomStatus="Booked"
                bookdata.save()
                return HttpResponse("Room Booked Successfully")

        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/') 
    

# menu card 
def menudata(request):
    try:
        if request.session['role']=="Teacher":

            Participants = request.POST['Participants']
            starttime = request.POST['starttime']
            Endtime = request.POST['Endtime']
            Comments = request.POST['Comments']
            Date = request.POST['date']
            foods= request.POST.getlist('food')
            data=MenuOrders(OrderParticipants=Participants,OrderComments=Comments,OrderList=foods,OrderStartDate=Date,OrderStartTime=starttime,OrderEndTime=starttime,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
            data.save()
            return HttpResponse('Order Book Successfully')

        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})
    
    except:
        return redirect('/') 
###################End Baloch################################

def midterm(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['title']   
                desct=request.POST['desct']
                startdate = request.POST['startdate']
                enddate = request.POST['enddate']   
                coursename=Course.objects.get(Cid=request.POST['category'])  
                mfile=request.FILES['mfile']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=MidtermModel(StartDate=startdate,EndDate=enddate,MidtermTitle=title,MidtermDesc=desct,MidtermFile=mfile,Course_id=coursename,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Mid Term Uploaded Successfully")
                return redirect('/faculty/midterm')
              
           

            
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            assignment=MidtermModel.objects.filter(Instructor_id=course_data.tid).order_by('-MidtermId')
            return render(request,'faculty/uploadmidtermexam.html',{'courses':courses,'assignment':assignment})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
    
def studentmidterm(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                courseid=request.POST['courses']
                data=Student_Midterm.objects.filter(Course_id=courseid)
                instructer_data=Instructor.objects.get(username=request.session['facultyuserid'])  
                course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
                # Instructor_courseid=list()
                # for x in course_data:
                #     Instructor_courseid.append(x.Cid)
                return render(request,'faculty/studentmidterm.html',{'course':course_data,'data':data})

            
            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            Instructor_courseid=list()
            for x in course_data:
                Instructor_courseid.append(x.Cid)
            data=Student_Midterm.objects.filter(Course_id__in=Instructor_courseid).order_by('-Student_Midterm_Id')
            return render(request,'faculty/studentmidterm.html',{'course':course_data,'data':data})
            

        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
        
        
#show student assignment

def showmidterm(request):
    if request.method == 'POST':
        marks=request.POST['marks']
        id = request.POST['sid']
        data=Student_Midterm.objects.get(Student_Midterm_Id=id)
        Midterm_File = request.FILES.get('file',False)
        if Midterm_File:
            data.Teacher_Upload=Midterm_File
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentmidterm')


        else:
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentmidterm')


    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Student_Midterm.objects.get(Student_Midterm_Id=uid)
        mydata=Ser_Midterms(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))
    
def finalexam(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                title=request.POST['title']   
                desct=request.POST['desct']
                startdate = request.POST['startdate']
                enddate = request.POST['enddate']   
                coursename=Course.objects.get(Cid=request.POST['category'])  
                mfile=request.FILES['mfile']
                instructor_id=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
                data=FinalExamModel(StartDate=startdate,EndDate=enddate,FinalExamTitle=title,FinalExamDesc=desct,FinalExamFile=mfile,Course_id=coursename,Instructor_id=instructor_id,uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
                data.save()
                messages.success(request,"Final Exam Uploaded Successfully")
                return redirect('/faculty/finalexam')
              
           

            
            course_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])   
            courses=Course.objects.filter(Instructor_id=course_data.tid)
            assignment=FinalExamModel.objects.filter(Instructor_id=course_data.tid).order_by('-FinalExamId')
            return render(request,'faculty/uploadfinalexam.html',{'courses':courses,'assignment':assignment})
            
        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
    
def studentfinalexam(request):
    try:
        if request.session['role']=="Teacher":
            if request.method=="POST":
                courseid=request.POST['courses']
                data=Student_FinalExam.objects.filter(Course_id=courseid)
                instructer_data=Instructor.objects.get(username=request.session['facultyuserid'])  
                course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
                # Instructor_courseid=list()
                # for x in course_data:
                #     Instructor_courseid.append(x.Cid)
                return render(request,'faculty/studentfinalexam.html',{'course':course_data,'data':data})

            
            instructer_data=Instructor.objects.get(username=request.session['facultyuserid'],uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])  
            course_data=Course.objects.filter(Instructor_id=instructer_data.tid)
            Instructor_courseid=list()
            for x in course_data:
                Instructor_courseid.append(x.Cid)
            data=Student_FinalExam.objects.filter(Course_id__in=Instructor_courseid).order_by('-Student_FinalExam_Id')
            return render(request,'faculty/studentfinalexam.html',{'course':course_data,'data':data})
            

        else:
            thank=True
            msg='Your are not a Teacher'
            return render(request,'index.html',{'thank':thank,'msg':msg})

    except:
        return redirect('/')
        
        
#show student assignment

def showfinalexam(request):
    if request.method == 'POST':
        marks=request.POST['marks']
        id = request.POST['sid']
        data=Student_FinalExam.objects.get(Student_FinalExam_Id=id)
        FinalExam_File = request.FILES.get('file',False)
        if FinalExam_File:
            data.Teacher_Upload=FinalExam_File
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentfinalexam')


        else:
            data.Mark=marks
            data.save()
            messages.success(request,"Uploaded marks Sucessfully")
            return redirect('/faculty/studentfinalexam')


    if request.method=="GET":    
        userdata=list()
        uid=request.GET['uid']
        data=Student_FinalExam.objects.get(Student_FinalExam_Id=uid)
        mydata=Ser_FinalExams(data)
        userdata.append(mydata.data)
        return HttpResponse(json.dumps(userdata))

# class meeting notification for student use pusher by shoaib ghulam
def classmeetingdata(request):
    return render(request,'faculty/meeting.html')


def onlineclass(request):

    instructorProfile=Instructor.objects.get(username=request.session['facultyuserid'])
    courses=Course.objects.filter(Instructor_id=instructorProfile.tid)
    studentBatch=Batch.objects.all()
    studentSamester=Semester.objects.all()
    alldata={
        'data':courses,
        'batch':studentBatch,
        'samester':studentSamester,
    }

    return render(request,'faculty/onlineclass.html',alldata)


# start meeting 
def startmeeting(request):
    if request.method=="POST":
        cid=request.POST['course']
        semester=request.POST['semester']
        batch=request.POST['batch']
        instructor=Instructor.objects.get(username=request.session['facultyuserid'])
        teacher="%s %s"%(instructor.First_Name, instructor.Last_Name)
        

        data= Student_Course.objects.filter(Courses=cid,StudenBatch=batch,Semester_ID=semester)
        coursename=data[0].Courses.all()
        teacherCourse=coursename[0].Course_name
        studentlist=list()
        for studentids in data:
            studentlist.append(studentids.Student_ID.User_id.user_id)
    
    #   crate host data for teacher join start
    
        # generating meeting user and  password start
        getmeeting=client.meeting.create(user_id="shoaibghulam45@gmail.com")
        meeting=getmeeting.json()
        meetingdata={
            'id':meeting['id'],
            'password': meeting['password'],
        }
        # generating meeting user and  password end
        
    #   crate host data for teacher join end
        # trager meeeting id and password to student
        # print(coursename)
        for ids in studentlist:
        
            pusher_client.trigger('chat'+str(ids), 'myevent', {'message':"hello owrld",'mid':meeting['id'],'password':meeting['password'],'instructor':teacher,'course':teacherCourse})
        
        request.session['hostdata']={
            'mid':meeting['id'],
            'password':meeting['password'],
            'role':1,
            'teacher':teacher,
        }
        return redirect('/faculty/meeting')

def meetingnotification(request):
    
   pass
def coursedatafatching(request):
    studentcourses=Student_Course.objects.filter(Courses__in=request.GET['cid'])
    data=SerStudentCourse(studentcourses, many=True)
    print(studentcourses)
    return HttpResponse(json.dumps(data.data))

@csrf_exempt
def meetingdata(request):
    r =json.loads(request.body) 
    mydata=r['meetingData']
    
    
    xdata = {
        'apiKey':mydata['apiKey'] ,
        'apiSecret': "kfpR6fi0K51zFLR5PaDvICFv2ekOQ9SLTaVl",
        'meetingNumber': mydata['meetingNumber'],
        'role':mydata['role'],
        'passWord':mydata['passWord'],
        
        }
    
    x=generateSignature(xdata);
    # print(x)
    # print(xdata)
   
    return HttpResponse(json.dumps(x))



# add student attendance system start  by shoaib ghulam
def addStudentatten(request):
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
            return redirect('attendance')
   
        
    
    except:
        return redirect('/university/')
    instructorProfile=Instructor.objects.get(username=request.session['facultyuserid'])
    courses=Course.objects.filter(Instructor_id=instructorProfile.tid)
    coursesid=list()
    for x in courses:
        coursesid.append(x.Cid)
    data= Student_Course.objects.filter(Courses__in=coursesid)
    # print(data[0])
    # coursename=data.all()
    student=Student_Profile.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    department=Department.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    # course=Course.objects.filter(uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    return render(request,'faculty/addStudentatten.html',{'student':data,'department':department,'course':courses})
    

# add student attendance system end
@csrf_exempt
def studentAttendanceData(request):
  
    sid=request.POST['sid']
    data= Student_Course.objects.get(Student_ID=sid,uniId=request.session['universityuniid'],branchId=request.session['universitybranchid'])
    serdata=SerStudentCourse(data , many=False)
   
    return HttpResponse(json.dumps(serdata.data))


    # quaiz sheet
def quizsheet(request,qid):
    request.session['qid']=qid
    print( request.session['qid'])
    return render(request,'faculty/quizsheet.html')
@csrf_exempt
def quizsheetsave(request):
    if request.method =="POST":
        save="nothing"
        question=request.POST['question']
        a1=request.POST['a1']
        a2=request.POST['a2']
        a3=request.POST['a3']
        a4=request.POST['a4']

        anwser=request.POST['anwser']
        uniId=request.session['universityuniid']
        branchId=request.session['universitybranchid'] 
        save=request.POST['save']
        
        data=quaizsheet(question=question,a1=a1,a2=a2,a3=a3,a4=a4,currectAnswse=anwser,quizid=onlinequiz.objects.get(onlinequizid=request.session['qid']),uniId=UniversityAccount.objects.get(UniId__in=request.session['facultyuniid']),branchId=UniversityBranch.objects.get(BranchId__in=request.session['facultybranchid']))
        data.save()
      
        return HttpResponse(save)
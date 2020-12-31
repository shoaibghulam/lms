from django.shortcuts import render, HttpResponse, redirect
from .models import Contact,User_Signup
from django.http import HttpResponse
from passlib.hash import pbkdf2_sha256
from django.core.mail import send_mail,EmailMultiAlternatives
from instructor.models import CourseCategory
from student.models import Student_Signup,Student_Profile
from faculty.models import User_Signup,Instructor
from UniversityApp.models import UniversityAccount,UniversityBranch
import json
import random
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        data=User_Signup.objects.get(username=username)
        password_encrpt=pbkdf2_sha256.hash(password)
        data.password=password_encrpt
        data.save()
        return redirect('/')
    data=CourseCategory.objects.all()
    return render(request,'index.html',{'data':data})

    
        

    
    
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        subject=request.POST['subject']
        data=Contact(Full_name=name,Email=email,subject=subject,Message=message)
        if data:
            data.save()
            Thank = True
            message="Your Response is Recorded"
            return render(request,'page-contact.html',{'message':message,'Thank':Thank})  
        else:
            
            message="Please Fill Correctly"
            return render(request,'page-contact.html',{'message':message,'Thank':Thank})  
    return render(request,'page-contact.html')
    

def pagecoursev2(request):
    return render(request,'page-course-v2.html')

def instructor(request):
    return render(request,'page-instructors.html')
def instructorsingle(request):
    return render(request,'page-instructors-single.html')

def coursev1(request):
    return render(request,'page-course-v1.html') 

def coursev2(request):
    return render(request,'page-course-v2.html') 

def coursev3(request):
    return render(request,'page-course-v3.html') 

def blog1(request):
    return render(request,'page-blog-v1.html')

def blog2(request):
    return render(request,'page-blog-grid.html')

def blog3(request):
    return render(request,'page-blog-list.html')

def single_post(request):
    return render(request,'page-blog-single.html')

def signup(request):
    if request.method=="POST":
        
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']
        password_encrpt=pbkdf2_sha256.hash(password)
        checkuser_name = User_Signup.objects.filter(username=username)
        checkuser_email = User_Signup.objects.filter(email=email)
        if checkuser_name or checkuser_email:
            thank=True
            msg="The username or email is already"
            return render(request,'index.html',{'msg':msg,'thank':thank})
           
        # mail verification
        token=random.randint(1000,100000)

        
        html_content=f'''
            <h1 style="text-align:center; font-family: 'Montserrat', sans-serif;">Finish creating your account</h1>
                <p> 
        Your email address has been registered with lms. To validate your account and activate your ability to send email campaigns, please complete your profile by clicking the link below:</p>
            <div style='width:300px; margin:0 auto;'> <a href='http://127.0.0.1:8000/verification/{token}/{username}' style=" background-color:#0066ff; border: none;  color: white; padding: 15px 32px;  text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-family: PT Sans, sans-serif;" >click here</a>
        </div>
            '''
        
        data=User_Signup(username=username,email=email,password=password_encrpt,token=token)
        data.save()
        thank=True
        msg="your account is successfully created please check your email and verify your account"
        subject, from_email, to = 'Verify Account', 'no-replay@gwadarengineeringworks.com', email
        msgsend = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msgsend.attach_alternative(html_content, "text/html")
        msgsend.send()
        
        return render(request,'index.html',{'msg':msg,'thank':thank})
        

    return redirect('/')
       


  
# def login(request):
#     if request.method=="POST":
#         email=request.POST['email']
#         password=request.POST['password']
#         try:
#             data=User_Signup.objects.get(email=email)
#             if data:
#                 encrpt=data.password
#                 role=data.role
#                 encrpt=pbkdf2_sha256.verify(password,encrpt)
#             if encrpt and role=="null":
#                 data=User_Signup.objects.get(email=email)
#                 request.session['username'] = data.username
#                 request.session['userid'] = data.sno
#                 request.session['role'] = data.role
#                 thank=True
#                 msg="Successfully Login"
#                 return render(request,'index.html',{'thank':thank,'msg':msg})
#             elif encrpt and role=="Teacher":
#                 data=User_Signup.objects.get(email=email)
#                 request.session['username'] = data.username
#                 request.session['userid'] = data.sno
#                 request.session['role'] = data.role
#                 thank=True
#                 msg="Successfully Login"
#                 return render(request,'dashboard/page-dashboard.html',{'thank':thank,'msg':msg})

#             else:
#                 thank=True
#                 msg="Password Incorrect"
#                 return render(request,'index.html',{'thank':thank,'msg':msg})
               
            
#         except User_Signup.DoesNotExist:
#             thank=True
#             msg="Email Doesnot Exist"
#             return render(request,'index.html',{'thank':thank,'msg':msg})

            
            
#     return redirect('/')

     
       
      
#     return redirect('/')

# verification 
def verification(request,verification,username):
    data= User_Signup.objects.get(username=username)
   
    if data.token==verification:
        updata= User_Signup.objects.get(username=username)
        updata.verify='verified'
        updata.save()
        return redirect('/login')
        
# end verification

# def error(request,slug):
#     return render(request,'page-error.html')

def forgetrequest(request):
    
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

def forget(request,verification,username):
    token=verification
    username=username
    return render(request,'forget.html',{'token':token,'username':username})

# def forgetcomplete(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         password=request.POST['password']
#         data=User_Signup.objects.get(username=username)
#         password_encrpt=pbkdf2_sha256.hash(password)
#         data.password=password_encrpt
#         data.save()
#         return HttpResponse('change')
#     return HttpResponse('not work')





def base(request):
    return render(request,'user/checking.html')

def studentlogin(request,name,username):
    
    try:
        if request.method=="POST":
            email=request.POST['email']
            password=request.POST['password']
            
            data=Student_Signup.objects.get(email=email,uniId__in=request.session['uniid'],branchId__in=request.session['branchid'])
            
            if data:
                if data.uniId.UniStatus=="Active":
                    if data.password==password:
                        image=Student_Profile.objects.get(User_id=data.user_id)
                        request.session['senderimg']=str(image.Profile)
                        request.session['username'] = data.username
                        request.session['userid'] = data.user_id
                        request.session['role'] = data.role
                        request.session['userrole'] = data.role
                        return redirect('/student')
                    else:
                        return redirect('studentlogin',name,username)
            else:
                return redirect('studentlogin',name,username)
    
        uniName = name
        branchUsername = username
        request.session['University'] = uniName
        request.session['Branch'] = branchUsername
       
        Uni = UniversityAccount.objects.filter(UniName=name)
        
        
        if Uni:

            Uniid = []
            for i in Uni:
                Uniid.append(i.UniId)
                request.session['logo'] = str(i.UniLogo)
               
           
            Branch = UniversityBranch.objects.filter(UniversityId__in=Uniid,BranchUsername=username)
            
            if Branch:
                BranchId = []
                for i in Branch:
                    BranchId.append(i.BranchId)
              
                request.session['branchid'] = BranchId
                request.session['uniid'] = Uniid
                return render(request,'studentlogin.html',{'name':uniName,'username':branchUsername})
                    
                
                
            else:
                return render(request,'page-error.html')

        else:
            return render(request,'page-error.html')
    
    except:
        return redirect('studentlogin',name,username)





def Facultylogin(request,name,username):

   
    try:
        if request.method=="POST":
           
            email=request.POST['email']
            password=request.POST['password']
            data=User_Signup.objects.get(email=email,uniId__in=request.session['facultyuniid'],branchId__in=request.session['facultybranchid'])
            
            if data:
                if data.uniId.UniStatus=="Active":
                    if data.password==password:
                        try:
                            image=Instructor.objects.get(username=data.user_id)
                            request.session['facultysenderimg']=str(image.img)
                        except:
                            None
                       
                        request.session['facultyusername'] = data.username
                        request.session['facultyuserid'] = data.user_id
                        request.session['role'] = data.role
                        request.session['userrole'] = data.role
                        return redirect('/faculty/')
                    else:
                        return redirect('Facultylogin',name,username)
            else:
                
                return redirect('Facultylogin',name,username)

        
        uniName = name
        branchUsername = username
        request.session['facultyUniversity'] = uniName
        request.session['facultyBranch'] = branchUsername
       
        Uni = UniversityAccount.objects.filter(UniName=name)
        if Uni:
            Uniid = []
            for i in Uni:
                Uniid.append(i.UniId)
                Uniid.append(i.UniId)
                request.session['logo'] = str(i.UniLogo)
                # request.session['facultylogo'] = str(i.UniLogo)
            Branch = UniversityBranch.objects.filter(UniversityId__in=Uniid,BranchUsername=username)
            if Branch:
                BranchId = []
                for i in Branch:
                    BranchId.append(i.BranchId)
                request.session['facultybranchid'] = BranchId
                request.session['facultyuniid'] = Uniid
                return render(request,'teacherlogin.html',{'name':uniName,'username':branchUsername})
                    
                
                
            else:
                return render(request,'page-error.html')

        else:
            return render(request,'page-error.html')

    except:
        uni = request.session['facultyUniversity']
        branch = request.session['facultyBranch']
        return redirect('Facultylogin',uni,branch)
       

def logout(request):
    try:
        del request.session['branchid']
        del request.session['uniid']
        del request.session['username']
        del request.session['userid']
        del request.session['role']
        del request.session['senderimg']
        uni = request.session['University']
        branch = request.session['Branch']
        return redirect('studentlogin',uni,branch)
    except:
        return redirect('studentlogin')

    

def logoutfaculty(request):
   
 
    try:
        del request.session['facultybranchid']
        del request.session['facultyuniid']
        del request.session['facultyusername']
        del request.session['facultyuserid']
        del request.session['role']
        del request.session['facultysenderimg']
        uni = request.session['facultyUniversity']
        branch = request.session['facultyBranch']
        return redirect('Facultylogin',uni,branch)
    except:
        uni = request.session['facultyUniversity']
        branch = request.session['facultyBranch']
        return redirect('Facultylogin',uni,branch)

# Finance Logins by shoaib ghulam
def FinanceLogin(request,uniuser,unibranch):
    # try:
    
    
    #  request.session['UniId'] 
     
        Uni = UniversityAccount.objects.get(UniUsername=uniuser)
        branch=UniversityBranch.objects.get(BranchUsername=unibranch)
        # x=str(Uni +" this is branch "+ branch)
        if branch.UniversityId.UniId==Uni.UniId:
            if Uni.UniStatus=="Active":

                request.session['financeuni'] = Uni.UniId
                request.session['financebranch'] = branch.BranchId
                return render(request,'finance/login.html')
              
            else:
                messages.error(request,"University account is disabled")
        return HttpResponse(branch)
    # except:
    #     return HttpResponse("this is excetption")
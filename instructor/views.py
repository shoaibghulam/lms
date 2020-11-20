from django.shortcuts import render,HttpResponse,redirect
from .models import teacher,CourseCategory,Course,videos,CourseLevel,SerTeacher,serVideos
from lmsapp.models import User_Signup
import json
import datetime
# Create your views here.
def dashboard(request):
    return render(request,'dashboard/page-dashboard.html')
def mycourses(request):
    
   return render(request,'dashboard/page-my-courses.html')
def myorder(request):
    return render(request,'dashboard/page-my-order.html')
def mymessages(request):
    return render(request,'dashboard/page-my-message.html')
def myreview(request):
    return render(request,'dashboard/page-my-review.html')
def mybookmarks(request):
    return render(request,'dashboard/page-my-bookmarks.html')
def mylisting(request):
    if request.method=="POST":
        title=request.POST['title']
        price=request.POST['price']
        duration=request.POST['duration']
        description=request.POST['description']
        requirment=request.POST['requirment']
        category=request.POST['cat']
        level=request.POST['level']
        thumbnail=request.FILES['thumbnail']
        instructor_id= request.session['userid']
        data=CourseCategory.objects.get(cattitle=category)
        category_id=data.catid
        data1=CourseLevel.objects.get(leveltitle=level)
        level_id=data1.levelid
        data2=Course(Course_title=title,Course_description=description,Course_requirment=requirment,Course_Price=price,Course_Duration=duration,Course_Thumbnail=thumbnail,instructor_id=User_Signup.objects.get(sno=instructor_id),Course_category=CourseCategory.objects.get(catid=category_id),Course_Level=CourseLevel.objects.get(levelid=level_id))
        data2.save()
        return redirect('/teacher')

    category=CourseCategory.objects.all()
    level=CourseLevel.objects.all()

    return render(request,'dashboard/page-my-listing.html',{'category':category,'level':level})



    # Become Instructer
def becomeinstructor(request):
    if request.method=="POST":
        uname=User_Signup.objects.get(sno=request.session['userid'])
        Name=request.POST['fullname']
        Occupation=request.POST['occupation']
        Company_Name=request.POST['companyname']
        Phone=request.POST['phone']
        Personal_info=request.POST['Personalinfo']
        Facebook=request.POST['fb']
        Twitter=request.POST['tw']
        Linkedin=request.POST['linkdin']
        Google_Plus=request.POST['googleplus']
        img=request.FILES['image']
        data=teacher(uname=uname,Name=Name,Occupation=Occupation,Company_Name=Company_Name,Phone=Phone,Personal_info=Personal_info,Facebook=Facebook,Twitter=Twitter,Linkedin=Linkedin,Google_Plus=Google_Plus,img=img)
        data.save()
        data1=User_Signup.objects.get(sno=request.session['userid'])
        data1.role="Teacher"
        data1.save()
        return redirect('/teacher')

    data=User_Signup.objects.get(sno=request.session['userid'])
    role=data.role
    if role=="Teacher":
        Thank=True
        return render(request,'dashboard/becomeinstructor.html',{'thank':Thank})

    else:
        return render(request,'dashboard/becomeinstructor.html')
def showinstructor(request):
     
    
    userdata = list()
    data=teacher.objects.filter(uname=User_Signup.objects.get(username=request.session['username']))
    if data:
        for x in data:
            datas=SerTeacher(x)
            userdata.append(datas.data)
        return HttpResponse(json.dumps(userdata))
 
def editinstructor(request):
  
    if request.method=="POST":
        data=teacher.objects.filter(uname=User_Signup.objects.get(username=request.session['username'])).update(Name=request.POST['fullname'],Occupation=request.POST['Occupation'],Company_Name=request.POST['Company'],Phone=request.POST['phone'],Personal_info=request.POST['info'],Facebook=request.POST['Facebook'],Twitter=request.POST['Twitter'],Linkedin=request.POST['linkdin'],Google_Plus=request.POST['googleplus'])
        
        return HttpResponse('Update Profile Suceesfully')


# Add videos into coures
def uploadvideo(request):
    
    data= Course.objects.filter(instructor_id=request.session['userid'])
    alldata={
        'data':data,
    }
    return render(request,'dashboard/add-courses.html',alldata)

def insertvideo(request):
    if request.method =='POST':
        title= request.POST['title']
        videofile= request.FILES['video']
        cid= Course.objects.get(course_id=request.POST['courseid'])
        insert=videos(videoTitle=title,videoFile=videofile,courseId=cid)
        insert.save()
        return HttpResponse("Video uploaded successfully")

# views upload views instructer page
def videosview(request):
    if request.method=='GET':
        # calculate video duration start
        # cap = cv2.VideoCapture('http://127.0.0.1:8000/upload/test.mp4')
        # seconds = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))
        # video_time = str(datetime.timedelta(seconds = seconds))
        # calculate video duration  end
        vid=request.GET['vid']
        data= videos.objects.filter(courseId=vid)
        videodata= serVideos(data, many=True)
       
        return HttpResponse(json.dumps(videodata.data))



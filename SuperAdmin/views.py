from django.shortcuts import render, HttpResponse, redirect
from passlib.hash import pbkdf2_sha256
from SuperAdmin.models import AdminAccount, Packages, Serpackage, Seradmin
from UniversityApp.models import UniversityAccount, UniversityBranch, SerUni, Serbranch
from faculty.models import User_Signup, SerFaculty
from student.models import Student_Signup
import json
from django.contrib import messages

# Create your views here.


def index(request):

    if not request.session.has_key('adminid'):
        return redirect('/superadmin/login')

    studentcount = Student_Signup.objects.all().count()
    facultycount = User_Signup.objects.all().count()
    universitycount = UniversityAccount.objects.all().count()
    branchcount = UniversityBranch.objects.all().count()
    return render(request, 'superadmin/home.html', {'studentcount': studentcount, 'facultycount': facultycount, 'universitycount': universitycount, 'branchcount': branchcount})


def university(request):
    if not request.session.has_key('adminid'):
        return redirect('/superadmin/login')

    package = Packages.objects.filter()
    return render(request, 'superadmin/university.html', {'package': package})


def universitybranch(request):
    if not request.session.has_key('adminid'):
        return redirect('/superadmin/login')
    return render(request, 'superadmin/branch.html')


def universitypakage(request):
    if not request.session.has_key('adminid'):
        return redirect('/superadmin/login')
    return render(request, 'superadmin/package.html')


def Profile(request):
    if not request.session.has_key('adminid'):
        return redirect('/superadmin/login')
    return render(request, 'superadmin/profile.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            data = AdminAccount.objects.get(SEmail=email)
            if data:
                if pbkdf2_sha256.verify(password, data.SPassword):
                    request.session['adminid'] = data.SId
                    request.session['adminname'] = data.SFname
                    request.session['adminimage'] = str(data.SProfile)
                    return redirect('/superadmin/')
                else:
                    messages.add_message(request, messages.INFO,
                                         'Please Enter Correct Password')
                    return redirect('/superadmin/login')
        except:
            messages.add_message(request, messages.INFO,
                                 'Please Enter Correct Email and Password')
            return redirect('/superadmin/login')

    return render(request, 'superadmin/login.html')


def logout(request):
    if  request.session.has_key('adminid'):
        del request.session['adminid']
        del request.session['adminimage']
        return redirect('/superadmin/login')
    else:
        return redirect('/superadmin/login')


def insert(request):
    if request.method == "POST":
        packagename = request.POST['packagename']
        price = request.POST['price']
        startdate = request.POST['sdate']
        enddate = request.POST['edate']
        flimit = request.POST['flimit']
        slimit = request.POST['slimit']
        desc = request.POST['desc']
        data = Packages(PackName=packagename, PackDescription=desc, PackStudent=slimit,
                        PackTeacher=flimit, PackDurationStart=startdate, PackDurationEnd=enddate, PackPrice=price)
        data.save()

        return HttpResponse('Package Sucessfully Added')


def show(request):
    userdata = list()
    data = Packages.objects.all().order_by('-PackId')[:]
    for x in data:
        datas = Serpackage(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))


def delete(request):
    uid = request.POST['uid']
    data = Packages.objects.filter(PackId=uid)
    data.delete()
    return HttpResponse("Delete Sucess")


def update(request):
    try:
        if request.method == "GET":
            userdata = list()
            uid = request.GET['uid']
            data = Packages.objects.get(PackId=uid)
            mydata = Serpackage(data)
            userdata.append(mydata.data)
            return HttpResponse(json.dumps(userdata))

        id = request.POST['uid']
        packagename = request.POST['upackagename']
        price = request.POST['uprice']
        startdate = request.POST['usdate']
        enddate = request.POST['uedate']
        flimit = request.POST['uflimit']
        slimit = request.POST['uslimit']
        desc = request.POST['udesc']

        getdata = Packages.objects.get(PackId=id)
        getdata.PackName = packagename
        getdata.PackPrice = price
        getdata.PackDurationStart = startdate
        getdata.PackDurationEnd = enddate
        getdata.PackTeacher = flimit
        getdata.PackStudent = slimit
        getdata.PackDescription = desc
        getdata.save()
        return HttpResponse('Update Successfully')

    except:
        None


def profileupdate(request):
    try:
        if request.method == "POST":
            data = AdminAccount.objects.get(SId=request.session['adminid'])
            firstname = request.POST['fname']
            lastname = request.POST['lname']
            email = request.POST['email']
            phone = request.POST['phone']
            uname = request.POST['uname']
            # img=request.FILES['img']

            data.SFname = firstname
            data.SLname = lastname
            data.SEmail = email
            data.SUsername = uname
            data.SContactNo = phone
            # data.SProfile=img
            data.save()
            return HttpResponse('Update Successfully')

        userdata = list()
        data = AdminAccount.objects.filter(SId=request.session['adminid'])
        for x in data:
            datas = Seradmin(x)
            userdata.append(datas.data)
        return HttpResponse(json.dumps(userdata))

    except:
        None


def activeuni(request):
    userdata = list()
    data = UniversityAccount.objects.filter(UniStatus="Active")
    for x in data:
        datas = SerUni(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))


def disableunistatus(request):
    userdata = list()
    data = UniversityAccount.objects.filter(UniStatus="Disable")
    for x in data:
        datas = SerUni(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))


def uniadd(request):
    if request.method == "POST":
        email = request.POST['email']
        checkrepeat = UniversityAccount.objects.filter(UniEmail=email)
        if checkrepeat:
            return HttpResponse('Email ALready Exist')
        uniname = request.POST['uniname']
        username = request.POST['username']
        password = request.POST['password']
        address = request.POST['address']
        package = Packages.objects.get(PackId=request.POST['package'])
        status = request.POST['status']
        image = request.FILES['image']
        id = AdminAccount.objects.get(SId=request.session['adminid'])
        data = UniversityAccount(UniName=uniname, UniUsername=username, UniEmail=email, UniPassword=password,
                                 UniAddress=address, UniStatus=status, UniLogo=image, UniPackage=package, SuperId=id)
        data.save()
        return HttpResponse('University Sucessfully Added')


def unishow(request):
    userdata = list()
    data = UniversityAccount.objects.all().order_by('-UniId')[:]
    for x in data:
        datas = SerUni(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))


def deleteuni(request):
    uid = request.POST['uid']
    data = UniversityAccount.objects.filter(UniId=uid)
    data.delete()
    return HttpResponse("Delete Successfully")


def updateuni(request):
    try:
        if request.method == "GET":
            userdata = list()
            uid = request.GET['uid']
            data = UniversityAccount.objects.get(UniId=uid)
            mydata = SerUni(data)
            userdata.append(mydata.data)
            return HttpResponse(json.dumps(userdata))

        id = request.POST['uid']
        email = request.POST['Uemail']
        checkrepeat = UniversityAccount.objects.filter(UniEmail=email)
        uniname = request.POST['Uuniname']
        username = request.POST['Uusername']
        password = request.POST['Upassword']
        address = request.POST['Uaddress']
        package = Packages.objects.get(PackId=request.POST['Upackage'])
        status = request.POST['Ustatus']
        image = request.FILES.get('Uimage', False)

        getdata = UniversityAccount.objects.get(UniId=id)
        getdata.UniName = uniname
        getdata.UniUsername = username
        getdata.UniPassword = password
        getdata.UniAddress = address
        getdata.UniEmail = email
        getdata.UniPackage = package
        getdata.UniStatus = status
        if image:
            getdata.UniLogo = image
        getdata.save()
        return HttpResponse('Update Successfully')

    except:
        None


def showpackagedetail(request):
    userdata = list()
    uid = request.GET['uid']
    data = Packages.objects.get(PackId=uid)
    mydata = Serpackage(data)
    userdata.append(mydata.data)
    return HttpResponse(json.dumps(userdata))


def disableuni(request):
    uid = request.GET['uid']
    data = UniversityAccount.objects.get(UniId=uid)
    data.UniStatus = "Disable"
    data.save()
    return HttpResponse("Disable Uni")


def activeunistatus(request):
    uid = request.GET['uid']
    data = UniversityAccount.objects.get(UniId=uid)
    data.UniStatus = "Active"
    data.save()
    return HttpResponse("Active Uni")

# show branch data


def branchdata(request):
    uid = request.POST['uid']
    userdata = list()
    data = UniversityBranch.objects.filter(UniversityId=uid)
    for x in data:
        datas = Serbranch(x)
        userdata.append(datas.data)
    return HttpResponse(json.dumps(userdata))


# show total teacher and student
def Count(request):
    bid = request.POST['bid']
    userdata = list()
    data = User_Signup.objects.filter(branchId=bid).count()
    data2 = Student_Signup.objects.filter(branchId=bid).count()
    userdata.append(data)
    userdata.append(data2)
    return HttpResponse(json.dumps(userdata))



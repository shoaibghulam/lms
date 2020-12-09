from django.shortcuts import render, HttpResponse, redirect
from UniversityApp.models import UniversityAccount, UniversityBranch, Serbranch
from student.models import Student_Signup
from faculty.models import User_Signup
from passlib.hash import pbkdf2_sha256
from django.contrib import messages
import json
from urllib.request import urlopen
import pandas as pd

# Create your views here.


def login(request):
    try:
        if request.method == "POST":

            email = request.POST['email']
            password = request.POST['password']

            data = UniversityAccount.objects.get(UniEmail=email)
            if data:
                if data.UniPassword == password:

                    request.session['UniId'] = data.UniId
                    request.session['Uniname'] = data.UniName
                    request.session['Uniimage'] = str(data.UniLogo)
                    return redirect('/branch/')
                else:
                     messages.error(request,"Enter Correct Username and password")
                     return redirect('/branch/login')

        return render(request, 'branch/login.html')
    except:
        messages.error(request,"Enter Correct Username and password")
        return redirect('/branch/login')


def logout(request):
    del request.session['UniId']
    return redirect('/branch/')


def index(request):
    if not request.session.has_key('UniId'):
        return redirect('/branch/login')
    branchcount = UniversityBranch.objects.filter(
        UniversityId=request.session['UniId']).count()
    Student = Student_Signup.objects.filter(
        uniId=request.session['UniId']).count()
    Teacher = User_Signup.objects.filter(
        uniId=request.session['UniId']).count()
    return render(request, 'branch/home.html', {'branchcount': branchcount, 'Student': Student, 'Teacher': Teacher})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()

    # data=UniversityAccount.objects.get(UniId=request.session['UniId'])
    # past=data.UniPackage.PackDurationEnd

    # if past >= present and data.UniStatus == "Active":
    #     branchcount=UniversityBranch.objects.filter(UniversityId=request.session['UniId']).count()
    #     return render(request,'branch/home.html',{'branchcount':branchcount})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def universitybranch(request):
    if not request.session.has_key('UniId'):
        return redirect('/branch/login')
    unidata=UniversityAccount.objects.get(UniId=request.session['UniId'])
    data = UniversityBranch.objects.filter(UniversityId=unidata.UniId).order_by('-BranchId')[:]
    return render(request, 'branch/branch.html', {'data': data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()

    # data=UniversityAccount.objects.get(UniId=request.session['UniId'])
    # past=data.UniPackage.PackDurationEnd

    # if past >= present and data.UniStatus == "Active":
    #     data=UniversityBranch.objects.filter(UniversityId=UniversityAccount.objects.get(UniId=request.session['UniId']))
    #     return render(request,'branch/branch.html',{'data':data})
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def profile(request):
    if not request.session.has_key('UniId'):
        return redirect('/branch/login')
    if request.method == 'POST':
        dataupdate = UniversityAccount.objects.get(UniId=request.session['UniId'])
        dataupdate.UniName= request.POST['UniName']
        dataupdate.UniPassword= request.POST['UniPassword']   
        dataupdate.UniAddress= request.POST['UniAddress']
        img=request.FILES.get('UniLogo',False)
        if img:
            dataupdate.UniLogo=request.FILES['UniLogo']
        dataupdate.save()
        if img:
            request.session['Uniimage'] = str(dataupdate.UniLogo)
        return redirect('profile')
    data = UniversityAccount.objects.get(UniId=request.session['UniId'])
    return render(request, 'branch/profile.html', {'data': data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()

    # data=UniversityAccount.objects.get(UniId=request.session['UniId'])
    # past=data.UniPackage.PackDurationEnd

    # if past >= present and data.UniStatus == "Active":

    #     return render(request,'branch/profile.html')
    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def profileshow(request):

    if request.method == "POST":
        if request.FILES.get('UniLogo') == None:
            data = UniversityAccount.objects.filter(UniId=request.session['UniId']).update(
                UniUsername=request.POST['UniUsername'], UniPassword=request.POST['UniPassword'], UniAddress=request.POST['UniAddress'])
        else:

            data = UniversityAccount.objects.get(
                UniId=request.session['UniId'])
            data.UniUsername = request.POST['UniUsername']
            data.UniPassword = request.POST['UniPassword']
            data.saveUniAddress = request.POST['UniAddress']
            data.UniLogo = request.FILES['UniLogo']
            data.save()
            request.session['Uniimage'] = str(data.UniLogo)

        messages.success(request, "Update Successfully")
        return redirect('/branch/profileshow')

    data = UniversityAccount.objects.filter(UniId=request.session['UniId'])
    return render(request, 'branch/profile.html', {'data': data})
    # result = urlopen('http://just-the-time.appspot.com/')
    # result = result.read().strip()
    # result_str = result.decode('utf-8')
    # present=result_str[:10]
    # present = pd.to_datetime(present).date()

    # data=UniversityAccount.objects.get(UniId=request.session['UniId'])
    # past=data.UniPackage.PackDurationEnd

    # if past >= present and data.UniStatus == "Active":
    #     data=UniversityAccount.objects.filter(UniId=request.session['UniId'])
    #     return render(request,'branch/profile.html',{'data':data})

    # else:
    #     data=UniversityAccount.objects.get(UniId=request.session['uniid'])
    #     data.UniStatus="Disable"
    #     data.save()
    #     return redirect('/university/login')


def addbranch(request):
    try:
        if request.method == "POST":
            BranchEmail = request.POST['BranchEmail']
            checkrepeat = UniversityBranch.objects.filter(
                BranchEmail=BranchEmail)
            if checkrepeat:

                messages.error(request, "Email ALready Exist")
                return redirect('/branch/universitybranch')
            BranchName = request.POST['BranchName']
            BranchUsername = request.POST['BranchUsername']
            BranchPassword = request.POST['BranchPassword']
            BranchAddress = request.POST['BranchAddress']
            BranchCreatedDate = request.POST['BranchCreatedDate']
            id = UniversityAccount.objects.get(UniId=request.session['UniId'])
            data = UniversityBranch(BranchName=BranchName, BranchUsername=BranchUsername, BranchEmail=BranchEmail,
                                    BranchPassword=BranchPassword, BranchAddress=BranchAddress, BranchCreatedDate=BranchCreatedDate, UniversityId=id)
            data.save()
            messages.success(request, " Successfully Added")
            return redirect('/branch/universitybranch')
    except:
        return redirect('/branch/')


def deletebranch(request, id):
    try:
        data = UniversityBranch.objects.filter(BranchId=id)
        data.delete()
        messages.error(request, "Delete Sucessfully")
        return redirect('/branch/universitybranch')
    except:
        return redirect('/branch/')


def show(request):
    try:
        userdata = list()
        id = request.GET['uid']
        data = UniversityBranch.objects.filter(BranchId=id)
        for x in data:
            datas = Serbranch(x)
            userdata.append(datas.data)
        return HttpResponse(json.dumps(userdata))
    except:
        return redirect('/branch/')


def editbranch(request):
    try:
        if request.method == "POST":
            BranchEmail = request.POST['UBranchEmail']
            checkrepeat = UniversityBranch.objects.filter(
                BranchEmail=BranchEmail)

            BranchName = request.POST['UBranchName']
            BranchUsername = request.POST['UBranchUsername']
            BranchEmail = request.POST['UBranchEmail']
            BranchPassword = request.POST['UBranchPassword']
            BranchAddress = request.POST['UBranchAddress']
            bid = request.POST['bid']
            data = UniversityBranch.objects.get(BranchId=bid)
            data.BranchName = BranchName
            data.BranchUsername = BranchUsername
            data.BranchEmail = BranchEmail
            data.BranchPassword = BranchPassword
            data.BranchAddress = BranchAddress
            data.save()
            messages.success(request, "Update Successfully")
            return redirect('/branch/universitybranch')
    except:
        return redirect('/branch/')

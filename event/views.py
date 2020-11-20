from django.shortcuts import render,HttpResponse
from .models import events
# Create your views here.
def event(request):
    data=events.objects.all()
    
    return render(request,'event/page-event.html',{'data':data})
def eventinfo(request,id):
     data=events.objects.filter(eventid=id)
     return render(request,'event/page-event-single.html',{'data':data})
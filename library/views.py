from django.shortcuts import render,HttpResponse

# Create your views here.
# Library Dashboard
def index(request):
    return HttpResponse("<h1>Library Dashboard</h1>")

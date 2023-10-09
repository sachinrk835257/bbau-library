from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    title = '''Home -'''
    return render(request,'index.html',{"title":title})

def register(request):
    title = '''Register'''
    if request.method == 'POST':
        messages.add_message(request, messages.SUCCESS, "yes")
        print("in register")
    return render(request,'register.html',{"title":title})

def adminLogin(request):
    title = '''Admin-Login'''
    if request.method == 'POST':
        messages.warning(request, "Your account expires in three days.")
        print("in admin login")
    return render(request,'adminLogin.html',{"title":title})

def dashboard(request):
    return render(request,"dashboard.html")

def regStudents(request):
    return render(request,'reg-students.html')

def editProfile(request):
    title = '''Admin-Login'''
    if request.method == "POST":
        return redirect('http://127.0.0.1:8000/registered-students/')
    return render(request,"edit-profile.html",{"title":title})

def delprofile(request,id):
    return redirect('http://127.0.0.1:8000/registered-students/')
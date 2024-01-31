from django.shortcuts import render ,redirect ,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Dashboard.models import Profile,Registered_Books, Issued_Books, Returned_Books,Department
from Authentication.models import ChangePassword,SuperUserReference
from Authentication.send_mail import send_mail
from uuid import uuid4
from django.utils import timezone
import pytz

# import datetime
current_time = timezone.now()
    # Convert it to the Indian timezone (Asia/Kolkata)
indian_time = current_time.astimezone(pytz.timezone('Asia/Kolkata'))


# Create your views here.
def user_login(request):
    title = '''BBAU SATELLITE | Login into Account'''
    print("yes found")
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            pswrd = request.POST.get('pswrd')
            if not User.objects.filter(username = email).exists():
                messages.add_message(request, messages.WARNING, "User Not Found !!!")
                return redirect('http://127.0.0.1:8000/user-login/')
            user = authenticate(request,username = email,password = pswrd, is_staff = False)
            if user is not None:
                user.last_login = indian_time #convert utc timzone into INDIAN timezone
                login(request,user)
                user.save()
                return redirect('http://127.0.0.1:8000/')
            
            else:
                print(user)
                messages.add_message(request, messages.WARNING, "INVALID CREDENTIALS !!!")
                return redirect('http://127.0.0.1:8000/user-login')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "Invalid Credentials !!!")
        return render(request,'user-login.html',{{"title":title}})


def addStudent(request):
    title = '''BBAU SATELLITE | Register'''

    department_obj = Department.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name').upper()
            gender = request.POST.get('gender').upper()
            semester = request.POST.get('semester').upper()

            depart = request.POST.get('depart').upper()
            library_id = request.POST.get('library_id')
            joiningYear = request.POST.get('joiningYear')
            passingYear = request.POST.get('passingYear')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            print(name,gender,depart)
            if pass1 != pass2:
                messages.add_message(request, messages.WARNING, "Password Mismatch !!!")
                return redirect('http://127.0.0.1:8000/authenticate/register/')
            
            if User.objects.filter(username = email).exists():
                messages.add_message(request, messages.WARNING, "Already Registered !!!")
                return redirect('http://127.0.0.1:8000/authenticate/register/')
            
            if Profile.objects.filter(library_id = library_id).exists():
                messages.add_message(request, messages.WARNING, "library id already Registered !!!")
                return redirect('http://127.0.0.1:8000/authenticate/register/')

            try:

                user = User.objects.create_user(username= email,email = email, is_staff = False)
                user.set_password(pass2)
                profile = Profile.objects.create(user = user,name = name,gender = gender, semester = semester, mobile = mobile, library_id = library_id, department = depart,joiningYear = joiningYear,passingYear = passingYear)
                

            except Exception as e:
                print(e)
                messages.add_message(request, messages.WARNING, "Error During reigistration !!!")
                return redirect('http://127.0.0.1:8000/authenticate/register/')
            

            profile.save()
            user.save()
            messages.add_message(request, messages.SUCCESS, "Registered Successfully")
            return redirect('http://127.0.0.1:8000/authenticate/register/')

        except Exception as e:
            messages.add_message(request, messages.WARNING, "{}".format(e))
            return redirect('http://127.0.0.1:8000/authenticate/register/')

    return render(request,'register.html',{"title":title,"Departments":department_obj})

# @user_passes_test(is_staff_member, login_url="http://127.0.0.1:8000/authenticate/admin-login/")
def adminRegister(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')

    title = '''BBAU SATELLITE | Admin Registeration'''
    try:
        if request.method == 'POST':    
            reference_by = request.POST.get('reference_by')     
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            libId = request.POST.get('libId')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            # pass1 = request.POST.get('pass1')
            # pass2 = request.POST.get('pass2')
            print(reference_by)
            # if pass1 != pass2:
            #     messages.add_message(request, messages.WARNING, "Password Mismatch !!!")
            #     return redirect('http://127.0.0.1:8000/authenticate/create-admin/')
            
            if User.objects.filter(username = email).exists():
                messages.add_message(request, messages.WARNING, "Already Registered !!!")
                return redirect('/')
            
            # user = User.objects.create_superuser(first_name = name, username= email,email = email, is_staff = True)
            # user.set_password(pass2)
            token = str(uuid4())
            superUser = SuperUserReference.objects.create(name = name,reference_by = reference_by, mobile = mobile, libraryId = libId, gender = gender,email = email,token = token)
            superUser.save()
            subject = "BBAU-LIBRARY Admin Reference"
            message = "Dear User"
            html_message = f'''<p>Reference by {reference_by}</P><p>Click on this link for set password credentials.</P><br><a href='http://127.0.0.1:8000/authenticate/admin-password/{token}'>http://127.0.0.1:8000/authenticate/admin-password/{token}</a><p style="color:red">Valid for 10 minutes only !!!</P>'''
            print(token)
            send_mail(email,subject, message, html_message)

            # messages.add_message(request, messages.SUCCESS, "Email sent successfully")
            messages.add_message(request, messages.SUCCESS, "Mail Sent Successfully.")
            return redirect('http://127.0.0.1:8000/authenticate/create-admin/')

    except Exception as e:
        messages.add_message(request, messages.WARNING, "{}".format(e))
        return redirect('http://127.0.0.1:8000/authenticate/create-admin/')

    return render(request,'register-admin.html',{"title":title})


def admin_login(request):
    title = '''BBAU SATELLITE | Admin Dashboard -'''
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            pswrd = request.POST.get('pswrd')
            isAdmin = request.POST.get('admin')
            if not isAdmin:
                messages.add_message(request, messages.WARNING, "Only Admins are allowed !!!")
                return redirect('http://127.0.0.1:8000/authenticate/admin-login/') 
            print(User.objects.filter(username = email).exists())
            if not User.objects.filter(username = email).exists():
                messages.add_message(request, messages.WARNING, "Admin Not Found !!!")
                return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
            user = authenticate(request,username = email,password = pswrd, is_staff = True)
            print(user)
            if user is not None:
                user.last_login = indian_time # Convert the UTC time to Indian Standard Time (IST)
                print(indian_time) 
                print(user.last_login)
                login(request,user)
                user.save()
                return redirect('http://127.0.0.1:8000/')
                # return render(request,'dashboard.html',{"title":title,"std_id":user.profile.id,"last_login_at":user.last_login})
            
            else:
                print(user)
                messages.add_message(request, messages.WARNING, "INVALID CREDENTIALS !!!")
                return redirect('http://127.0.0.1:8000/authenticate/admin-login/')

    except Exception as e:
        messages.add_message(request, messages.WARNING, "Invalid Credentials ")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    return render(request,'admin-login.html',{"title":title})

def setPassword(request,passToken):
    print("email change password")
    title = '''BBAU SATELLITE | Set Password'''
    try:
        super_user_obj = SuperUserReference.objects.get(token = passToken)
        if request.method == 'POST':
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if pass1 != pass2:
                messages.add_message(request, messages.WARNING, "Password Mismatch !!!")
                return redirect('http://127.0.0.1:8000/authenticate/admin-password/{}'.format(passToken))
            
            if User.objects.filter(username = super_user_obj.email).exists():
                messages.add_message(request, messages.WARNING, "Already Registered !!!")
                return redirect('/')
            
            user = User.objects.create_superuser(first_name = super_user_obj.name, username= super_user_obj.email,email = super_user_obj.email, is_staff = True)
            user.set_password(pass2)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Password Set successfully")
            return redirect('http://127.0.0.1:8000/authenticate/admin-password/{}'.format(passToken))
    except Exception as e:
        messages.add_message(request, messages.WARNING, "Some technical error . Try again after some time  !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-password/{}'.format(passToken))
    return render(request,'admin-password.html',{"title":title,"email":super_user_obj.email})
    

def forgotChangePassword(request,token):
    print("email change password")
    title = '''BBAU SATELLITE | change password'''
    try:
        user_obj = ChangePassword.objects.get(token = token)
        if request.method == 'POST':
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if pass1 != pass2:
                messages.add_message(request, messages.WARNING, "Password Mismatch !!!")
                return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(token))
            user =  User.objects.get(username = user_obj.email)
            user.set_password(pass2)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Password Change successfully")
            return redirect('/')
        return render(request,'email-change-password.html',{"title":title,"username":user_obj.email})
    except Exception as e:
        messages.add_message(request, messages.WARNING, "Some technical error . Try again after some time  !!")
        return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(token))


@login_required(login_url='http://127.0.0.1:8000/')
def changePassword(request,id):
    print("in change password",id)
    title = '''BBAU SATELLITE | change password'''
    try:
        user_obj = User.objects.get(id = id)
        print(user_obj)
        if request.method == 'POST':
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            pass3 = request.POST.get('pass3')
            if pass2 != pass3:
                messages.add_message(request, messages.WARNING, "Password Mismatch !!!")
                return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))
            
            subject = "BBAU-LIBRARY | Change Password"
            message = "Dear User"
            html_message = f'''<p>You have change your password successfully</P><p style="color:red">Contact library incharge if you are not?!!!</P>'''
            if (request.user.is_superuser):
                user = authenticate(request,username = email,password = pass1, is_staff = True)
                if user is not None:
                    user.set_password(pass3)
                    user.save()
                    send_mail(email,subject, message, html_message)
                    messages.add_message(request, messages.SUCCESS, "Password Change successfully")
                    return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))
                
                messages.add_message(request, messages.WARNING, "INVALID CREDENTIALS !!!")
                return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))
            else:
                user = authenticate(request,username = email,password = pass1, is_staff = False)
                if user is not None:
                    user.set_password(pass3)
                    user.save()
                    send_mail(email,subject, message, html_message)
                    messages.add_message(request, messages.SUCCESS, "Password Change successfully")
                    return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))

            
                messages.add_message(request, messages.WARNING, "INVALID CREDENTIALS !!!")
                return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))

    except Exception as e:
        messages.add_message(request, messages.WARNING, "Some technical error . Try again after some time  !!")
        return redirect('http://127.0.0.1:8000/authenticate/change-password/{}'.format(id))
    
    return render(request,'change-password.html',{"title":title,"username":user_obj.email})


def logout_page(request):
    logout(request)
    return redirect('/')
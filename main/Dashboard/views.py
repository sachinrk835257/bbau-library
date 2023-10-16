from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books
from Authentication.send_mail import send_mail
from Authentication.models import ChangePassword
from uuid import uuid4

# Create your views here.
def index(request):
    title = '''Home -'''
    if request.user.is_authenticated :
        print("in authenticated")
        title = '''Dashboard-'''
        staff_status = "User"       #DEfault
        book_obj = Registered_Books.objects.all().count()
        if (request.user.is_superuser) :
            staff_status = "Admin"
            print("in superUser")
            profile_count = Profile.objects.all().count()
            return render(request,"index.html",{"title":title,"staff_status":staff_status,"registeredUsers":profile_count,"bookListedNumbers":book_obj})

        return render(request,"index.html",{"title":title,"staff_status":staff_status,"bookListedNumbers":book_obj})

    print("in home")
    return render(request,'index.html',{"title":title})

def regStudents(request):
    title = '''Registered Students'''
    students = Profile.objects.all()
    print(students)

    return render(request,'registered-students.html',{"title":title,"students":students})

def editProfile(request,myid):
    title = '''Edit-Profile'''
    profile = Profile.objects.get(library_id = myid)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            department = request.POST.get('department')
            joiningYear = request.POST.get('joiningYear')
            passingYear = request.POST.get('passingYear')
            mobile = request.POST.get('mobile')
            print(name,department,mobile,joiningYear,passingYear)
                        
            profile.name = name
            profile.department = department
            profile.joiningYear = joiningYear
            profile.mobile = mobile
            profile.passingYear = passingYear
            profile.save()
        
            messages.add_message(request, messages.SUCCESS, "Profile Update Successfully")
            print("yes done")
            return redirect('http://127.0.0.1:8000/edit-profile/{}'.format(myid))

        except Exception as e:
            messages.add_message(request, messages.WARNING, "{}".format(e))
            return redirect('http://127.0.0.1:8000/edit-profile/{}'.format(myid))
    return render(request,"profile.html",{"title":title,"profile":profile})

def delprofile(request,myid):
    profile = Profile.objects.filter(id = myid)
    # profile = Profile.objects.filter(id = myid).delete()
    profile.delete()
    # profile.save()

    return redirect('http://127.0.0.1:8000/registered-students/')

def forgotPassword(request):
    title = '''forgot Password'''
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.filter(username = email).exists()
            if not user:
                messages.add_message(request, messages.WARNING, "User not found. Please register first !")
                return redirect('/')
        
            subject = "BBAU-LIBRARY Change Password"
            message = "Dear User"
            token = str(uuid4())
            html_message = "<p>You can change password from link provided below click on that and further proceed</P><br><a href='http://127.0.0.1:8000/authenticate/change-password/{}'>http://127.0.0.1:8000/authenticate/change-password/{}</a>".format(token,token)
            send_mail(email,subject, message, html_message)
            messages.add_message(request, messages.SUCCESS, "Email sent successfully")
            user_obj = ChangePassword.objects.create(email = email,token = token)
            user_obj.save()
            return redirect('http://127.0.0.1:8000/forgot-password/')
    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "User not found. Please register first !")
        return redirect('/')
        
    return render(request,'forgot-password.html')


def addBook(request):

    title = '''adding book'''
    try:
        if request.method == 'POST':
            bookName = request.POST.get('bookName')
            department = request.POST.get('department')
            category = request.POST.get('category')
            isbn = request.POST.get('ISBN')
            authorName = request.POST.get('authorName')
            bookPrice = request.POST.get('bookPrice')
            coverImage = request.FILES['coverImage']
           


            if coverImage:
                print(bookName,department,category,isbn,authorName,bookPrice,coverImage)    
                book_obj = Registered_Books.objects.create(register_by = request.user.first_name, bookName = bookName,department = department, category = category, ISBN = isbn, authorName = authorName, bookPrice = bookPrice, coverImage =coverImage)
                book_obj.save()
                messages.add_message(request, messages.SUCCESS, "Book Added Successfully")
                return redirect('http://127.0.0.1:8000/add-book/')
            else:
                messages.add_message(request, messages.WARNING, "Please Upload an Image !!!")
                return redirect('http://127.0.0.1:8000/add-book/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "Some Error !!!")
        return redirect('http://127.0.0.1:8000/add-book/')
    
    return render(request,'add-book.html',{"title":title})


def deleteBook(request,isbn):
    book_obj = Registered_Books.objects.get(ISBN = isbn).delete()

    return redirect('http://127.0.0.1:8000/manage-book/')

def deleteProfile(request,myid):
    profile = Profile.objects.get(library_id = myid)
    
    User.objects.get(id = profile.user.id).delete()

    return redirect('http://127.0.0.1:8000/registered-students/')

def listedBooks(request):
    if request.user.is_authenticated:
        title = '''Registered Books'''
        book_obj = Registered_Books.objects.all()
        
        return render(request,'registered-books.html',{"title":title,"books":book_obj})

def manageBook(request):
    title = '''Manage Book'''
    if request.user.is_superuser:
        title = '''Registered Books'''
        book_obj = Registered_Books.objects.all()
        
        return render(request,'manage-book.html',{"title":title,"books":book_obj})


def bookDetails(request,isbn):
    title = '''Update Books Details'''
    print(isbn)
    book_obj1 = Registered_Books.objects.get(ISBN = isbn)
    print(book_obj1.category)
    try:
        if request.method == 'POST':
            bookName = request.POST.get('bookName')
            department = request.POST.get('department')
            category = request.POST.get('category')
            authorName = request.POST.get('authorName')
            bookPrice = request.POST.get('bookPrice')
                           
            print("not in cover image")
            print(bookName,department,category,isbn,authorName,bookPrice)  
            book_obj1.bookName = bookName
            book_obj1.authorName = authorName
            book_obj1.category = category
            book_obj1.department = department
            book_obj1.bookPrice = bookPrice
            book_obj1.save()

            if request.FILES['coverImage']:
                print("in cover image") 
                book_obj1.coverImage = request.FILES['coverImage']
                book_obj1.save()

            messages.add_message(request, messages.SUCCESS, "Book Updated Successfully")
            return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))

    except Exception as e:
        print(e)
        messages.add_message(request, messages.SUCCESS, "Book Updated Successfully")
        return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))
    
    return render(request,'book-detail.html', {"title":title,"book":book_obj1})

def searchBy(request):
    title = '''Registered Books'''
    if request.method == 'POST':
        search = request.POST.get('search-by')
        print(search)
        book_obj1 = Registered_Books.objects.filter(bookName__contains = search)
        book_obj2 = Registered_Books.objects.filter(ISBN__contains = search)
        book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        book_obj4 = Registered_Books.objects.filter(department__contains = search)
        book_obj5 = Registered_Books.objects.filter(category__contains = search)
        union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5
        print(union_queryset)

        return render(request,'registered-books.html',{"title":title,"books":union_queryset})
    
def applyFilter(request):
    title = '''Registered Books'''
    if request.method == 'POST':
        sort_by = request.POST.get('sort-by')
        
        book_obj1 = Registered_Books.objects.all().order_by(sort_by)
        # print(book_obj1)
        # book_obj2 = Registered_Books.objects.filter(ISBN__contains = search)
        # book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        # book_obj4 = Registered_Books.objects.filter(department__contains = search)
        # book_obj5 = Registered_Books.objects.filter(category__contains = search)
        # union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5

        return render(request,'registered-books.html',{"title":title,"books":book_obj1})
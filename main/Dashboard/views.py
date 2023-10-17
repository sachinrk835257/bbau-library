from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from Authentication.send_mail import send_mail
from Authentication.models import ChangePassword
from uuid import uuid4
from django.utils import timezone

# Create your views here.
def index(request):
    title = '''Home -'''
    if request.user.is_authenticated :
        title = '''Dashboard-'''
        staff_status = "User"       #DEfault
        book_obj = Registered_Books.objects.all().count()
        if (request.user.is_superuser) :
            staff_status = "Admin"
            profile_count = Profile.objects.all().count()
            return render(request,"index.html",{"title":title,"staff_status":staff_status,"registeredUsers":profile_count,"bookListedNumbers":book_obj})

        return render(request,"index.html",{"title":title,"staff_status":staff_status,"bookListedNumbers":book_obj})
    
    else:
        messages.add_message(request, messages.WARNING, "Login First !!!")
        return render(request,'index.html',{"title":title})

def regStudents(request):
    title = '''Registered Students'''
    students = Profile.objects.all()
    print(students)

    return render(request,'registered-students.html',{"title":title,"students":students})


@login_required(login_url="http://127.0.0.1:8000/")
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
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
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
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
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
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    book_obj = Registered_Books.objects.get(ISBN = isbn).delete()

    return redirect('http://127.0.0.1:8000/manage-book/')

def deleteProfile(request,myid):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    profile = Profile.objects.get(library_id = myid)
    
    User.objects.get(id = profile.user.id).delete()

    return redirect('http://127.0.0.1:8000/registered-students/')

@login_required(login_url='http://127.0.0.1:8000/')
def listedBooks(request):
    if request.user.is_authenticated:
        title = '''Registered Books'''
        book_obj = Registered_Books.objects.all()
        print(book_obj[0].status)
        
        return render(request,'registered-books.html',{"title":title,"books":book_obj})


def manageBook(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''Manage Book'''
    if request.user.is_superuser:
        title = '''Registered Books'''
        book_obj = Registered_Books.objects.all()
        
        return render(request,'manage-book.html',{"title":title,"books":book_obj})


def bookDetails(request,isbn):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
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


@login_required(login_url='http://127.0.0.1:8000/')
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


@login_required(login_url='http://127.0.0.1:8000/')  
def applyFilter(request):
    title = '''Registered Books'''
    if request.method == 'POST':
        sort_by = request.POST.get('sort-by')
        
        book_obj1 = Registered_Books.objects.all().order_by(sort_by)
        return render(request,'registered-books.html',{"title":title,"books":book_obj1})
    

def issueBook(request):
    print(" in issue book funtion")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''Issue Book'''

    try:
        if request.method == 'POST':
            print("posted")
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            print(ISBN,library_id)
            found = True
            book_obj = Registered_Books.objects.filter(ISBN = ISBN)
            profile_obj = Profile.objects.filter(library_id = library_id)
            if not book_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Book Not Found !!!")

            if not profile_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Both Book and Student Not Found !!!")

            return render(request,'issue-book.html',{"title":title,"book":book_obj,"student":profile_obj,"found":found})

    except Exception as e:
        return redirect('/')

    

def issuingBook(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    try:
        if request.method == 'POST':
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            

            book_obj = Registered_Books.objects.get(ISBN = ISBN)
            profile_obj = Profile.objects.get(library_id = library_id)   

            profile_obj.issuedBooks = profile_obj.issuedBooks + 1
            book_obj.last_issued_by = profile_obj.name
            print(book_obj.status)
            book_obj.status = "Not Available"
            print(book_obj.status)

            issued_book_obj = Issued_Books.objects.create(issued_by = profile_obj.name, email = profile_obj.user.email, mobile = profile_obj.mobile, issue_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN, category = book_obj.category )

            book_obj.save()
            print(book_obj.status)
            profile_obj.save()
            issued_book_obj.save()

            return redirect('http://127.0.0.1:8000/issued-books/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.SUCCESS, "Some Error !!")
        return redirect('http://127.0.0.1:8000/')
    
    
def returnBook(request):
    print(" in return book funtion")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''Issue Book'''

    try:
        if request.method == 'POST':
            print("posted")
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            print(ISBN,library_id)
            found = True
            book_obj = Registered_Books.objects.filter(ISBN = ISBN)
            profile_obj = Profile.objects.filter(library_id = library_id)
            if not book_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Book Not Found !!!")

            if not profile_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Both Book and Student Not Found !!!")

            return render(request,'return-book.html',{"title":title,"book":book_obj,"student":profile_obj,"found":found})

    except Exception as e:
        return redirect('/')
    

def returningBook(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    try:
        if request.method == 'POST':
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')

            book_obj = Registered_Books.objects.get(ISBN = ISBN)
            profile_obj = Profile.objects.get(library_id = library_id)   

            profile_obj.returnedBooks = profile_obj.returnedBooks + 1
            print(book_obj.status)
            Registered_Books.objects.update(last_issued_by = profile_obj.name, status = 'Available')
            print(book_obj.status)

            returned_books_obj = Returned_Books.objects.create(returned_by = profile_obj.name, email = profile_obj.user.email, mobile = profile_obj.mobile, return_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN, category = book_obj.category )

            book_obj.save()
            print(book_obj.status)
            profile_obj.save()
            returned_books_obj.save()

            return redirect('http://127.0.0.1:8000/returned-books/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.SUCCESS, "Some Error !!")
        return redirect('http://127.0.0.1:8000/')
    
def issuedBooks(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU-LIBRARY | Issued Books'''
    issued_book_obj = Issued_Books.objects.all().count()

    return render(request,'issued-books.html',{"title":title,"issuedBooksNumbers":issued_book_obj})
    
def returnedBooks(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU-LIBRARY | Returned Books'''
    returned_books_obj = Returned_Books.objects.all().count()

    return render(request,'returned-books.html',{"title":title,"returnedBooksNumbers":returned_books_obj})
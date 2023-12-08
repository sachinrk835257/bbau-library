from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books, Department
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from Authentication.send_mail import send_mail
from Authentication.models import ChangePassword
from uuid import uuid4
from django.utils import timezone
from django.db.models import Count,Q

# Create your views here.
def about(request):
    title = '''BBAU SATELLITE | About Us'''
    return render(request,'about-us.html',{"title":title})

def userLogin(request):
    title = '''BBAU SATELLITE | Login Page'''
    return render(request,'user-login.html',{"title":title})

def index(request):
    print("home")
    title = '''BBAU SATELLITE | Home -'''
    if request.user.is_authenticated :
        title = '''BBAU SATELLITE | Dashboard-'''
        staff_status = "Student"       #DEfault
        user_obj = User.objects.get(email = request.user.email)
        book_obj = Registered_Books.objects.all().count()
        issued_books_obj = Issued_Books.objects.all().count()
        returned_books_obj = Returned_Books.objects.all().count()
        print(issued_books_obj,returned_books_obj)
        profile_count = Profile.objects.all().count()
        
        if (request.user.is_superuser) :
            staff_status = "Admin"
            # author_name = Registered_Books.objects.values("authorName").distinct()
            # print(book_name)
            # print(author_name)
            # print(Count)
            return render(request,"index.html",{"title":title,"staff_status":staff_status,"registeredUsers":profile_count,"bookListedNumbers":book_obj,"returnedBooks":returned_books_obj,"issuedBooks":issued_books_obj})
        

        profile_obj = Profile.objects.get(library_id = request.user.profile.library_id)
        if profile_obj.issuedBooks == 'Null':
                profile_obj.issuedBooks = ""

        if profile_obj.returnedBooks == 'Null':
            profile_obj.returnedBooks = ""
        
        profile_obj.save()
        issuedBooks = (profile_obj.issuedBooks)
        listOfIssueBook = issuedBooks.split()
        print("list",listOfIssueBook)
        returnedBooks = profile_obj.returnedBooks
        listOfReturnBook = returnedBooks.split()
        print("vvvv   ",len(listOfReturnBook))
        return render(request,"index.html",{"title":title,"staff_status":staff_status,"bookListedNumbers":book_obj,"issuedBooks":len(listOfIssueBook),"returnedBooks":len(listOfReturnBook),"registeredUsers":profile_count})
    
    else:
        messages.add_message(request, messages.WARNING, "Login First !!!")
        return render(request,'index.html',{"title":title})

def regStudents(request):
    title = '''BBAU SATELLITE | Registered Students'''
    students = Profile.objects.all()
    print(students)

    return render(request,'registered-students.html',{"title":title,"students":students})


@login_required(login_url="http://127.0.0.1:8000/")
def editProfile(request,myid):
    title = '''BBAU SATELLITE | Edit-Profile'''
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
    title = '''BBAU SATELLITE | forgot Password'''
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = User.objects.filter(username = email).exists()
            if not user:
                messages.add_message(request, messages.WARNING, "User not found. Please register first !")
                return redirect('http://127.0.0.1:8000/user-login/')
        
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
    title = '''BBAU SATELLITE | adding book'''
    department_obj = Department.objects.all()
    try:
        if request.method == 'POST':
            bookName = request.POST.get('bookName')
            department = request.POST.get('department')
            
            isbn = request.POST.get('ISBN')
            if (" " in isbn or "," in isbn):
                messages.add_message(request, messages.WARNING, "ISBN without characters of \'  \', or \' , \' !!!")
                return redirect('http://127.0.0.1:8000/add-book/')

            authorName = request.POST.get('authorName')
            bookPrice = request.POST.get('bookPrice')
            coverImage = request.FILES['coverImage']
           


            if coverImage:
                # print(bookName,department,isbn,authorName,bookPrice,coverImage)    
                book_obj = Registered_Books.objects.create(register_by = request.user.first_name, bookName = bookName,department = department, ISBN = isbn, authorName = authorName, bookPrice = bookPrice, coverImage =coverImage)

                if department == "COMPUTER SCIENCE" or department == "INFORMATION TECHNOLOGY":
                    category = request.POST.get('category')
                    book_obj.category = category
                book_obj.save()
                messages.add_message(request, messages.SUCCESS, "Book Added Successfully")
                return redirect('http://127.0.0.1:8000/add-book/')
            else:
                messages.add_message(request, messages.WARNING, "Please Upload an Image !!!")
                return redirect('http://127.0.0.1:8000/add-book/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "ISBN should be Unique OR Technical Error !!!")
        return redirect('http://127.0.0.1:8000/add-book/')
    
    return render(request,'add-book.html',{"title":title,"Departments":department_obj})

def addMultiple(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU SATELLITE | adding Multiple book'''
    department_obj = Department.objects.all()
    try:
        if request.method == 'POST':
            bookName = request.POST.get('bookName')
            department = request.POST.get('department')
            
            isbn = request.POST.get('ISBN')
            print(isbn,type(isbn))
            if "," in isbn:
                isbn = ''.join(isbn.split())
                isbn = isbn.split(',')
                print(isbn)
            else:
                messages.add_message(request, messages.WARNING, "unique ISBN should be written with comma seperated  !!!")
                return redirect('http://127.0.0.1:8000/multiple-entry/')
            
            authorName = request.POST.get('authorName')
            bookPrice = request.POST.get('bookPrice')
            coverImage = request.FILES['coverImage']
           
            if coverImage:
                print(bookName,department,isbn,authorName,bookPrice,coverImage)   

                for b in isbn:
                    book_obj = Registered_Books.objects.create(register_by = request.user.first_name, bookName = bookName,department = department, ISBN = b, authorName = authorName, bookPrice = bookPrice, coverImage =coverImage)

                    if department == "COMPUTER SCIENCE" or department == "INFORMATION TECHNOLOGY":
                        category = request.POST.get('category')
                        book_obj.category = category
                    book_obj.save()
                messages.add_message(request, messages.SUCCESS, "Book Added Successfully")
                return redirect('http://127.0.0.1:8000/multiple-entry/')
            else:
                messages.add_message(request, messages.WARNING, "Please Upload an Image !!!")
                return redirect('http://127.0.0.1:8000/multiple-entry/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "ISBN should be Unique OR Technical Error !!!")
        return redirect('http://127.0.0.1:8000/add-book/')
    
    return render(request,'add-same-book.html',{"title":title,"Departments":department_obj})

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
    print("in Listed books")
    if request.user.is_authenticated:
        title = '''BBAU SATELLITE | Registered Books'''
        book_obj = Registered_Books.objects.all()
        print(book_obj.count())
        same_books = book_obj.values('bookName','authorName','department').annotate(book_count = Count("pk"), availability_count=Count('id', filter=Q(status='Available')),
        not_availability_count=Count('id', filter=Q(status='Not Available'))).filter(book_count__gt=1)
        print(same_books,type(same_books))
        bookName = []
        authorName = []
        coverImages = {}
        for i in same_books:
            bookName.append(i["bookName"])
            authorName.append(i["authorName"])
            coverImages["img"] = (book_obj.filter(bookName = i["bookName"], authorName = i["authorName"]).first().coverImage)
        copy_books = book_obj.filter(bookName__in = bookName,authorName__in = authorName)
        print("****")
        print(bookName,authorName)
        print(copy_books.values("bookName").distinct())
        print("****")
        print(type(coverImages),coverImages)
        print(copy_books.count())
        exclude_copy_books = book_obj.exclude(pk__in = copy_books.values('pk'))
        print(exclude_copy_books)

        return render(request,'registered-books.html',{"title":title,"sameBooks":same_books,"coverImages":coverImages,"remainingBooks":exclude_copy_books})


def manageBook(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU SATELLITE | Manage Book'''
    if request.user.is_superuser:
        title = '''BBAU SATELLITE | Registered Books'''
        book_obj = Registered_Books.objects.all()
        
        return render(request,'manage-book.html',{"title":title,"books":book_obj})


def bookDetails(request,isbn):
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    title = '''BBAU SATELLITE | Update Books Details'''
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
def searchByRegisteredBooks(request):
    title = '''BBAU SATELLITE | Registered Books'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by')
        print(search)
        book_obj1 = Registered_Books.objects.filter(bookName__contains = search)
        book_obj2 = Registered_Books.objects.filter(ISBN__contains = search)
        book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        book_obj4 = Registered_Books.objects.filter(department__contains = search)
        book_obj5 = Registered_Books.objects.filter(category__contains = search)
        book_obj5 = Registered_Books.objects.filter(status = search.lower())
        union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5
        print(union_queryset)

        return render(request,'registered-books.html',{"title":title,"books":union_queryset})
    
@login_required(login_url='http://127.0.0.1:8000/')
def searchByManageBooks(request):
    title = '''BBAU SATELLITE | Manage Books'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by')
        print(search)
        book_obj1 = Registered_Books.objects.filter(bookName__contains = search)
        book_obj2 = Registered_Books.objects.filter(ISBN__contains = search)
        book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        book_obj4 = Registered_Books.objects.filter(department__contains = search)
        book_obj5 = Registered_Books.objects.filter(status = search.lower())
        union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5
        print(union_queryset)

        return render(request,'registered-books.html',{"title":title,"books":union_queryset})

@login_required(login_url='http://127.0.0.1:8000/')
def searchByRegisteredStudents(request):
    title = '''BBAU SATELLITE | Registered Students'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by')
        print(search)
        book_obj1 = Profile.objects.filter(name__contains = search)
        book_obj2 = Profile.objects.filter(library_id__contains = search)
        book_obj4 = Profile.objects.filter(department__contains = search)
        union_queryset = book_obj1 | book_obj2 | book_obj4 
        print(union_queryset)

        return render(request,'registered-students.html',{"title":title,"books":union_queryset})

    
@login_required(login_url='http://127.0.0.1:8000/')  
def sortByRegisteredBooks(request):
    title = '''BBAU SATELLITE | Registered Books'''
    if request.method == 'POST':
        sort_by = request.POST.get('sort-by')
        print(sort_by)
        # book_obj2 = Registered_Books.objects.filter(status = sort_by)
        book_obj1 = Registered_Books.objects.all().order_by(sort_by)
        union_queryset = book_obj1 
        return render(request,'registered-books.html',{"title":title,"books":union_queryset})

    
@login_required(login_url='http://127.0.0.1:8000/')  
def sortByManageBooks(request):
    title = '''BBAU SATELLITE | Apply FIlter Manage books'''
    if request.method == 'POST':
        sort_by = request.POST.get('sort-by')
        print(sort_by)
        
        # book_obj2 = Registered_Books.objects.filter(status = sort_by)
        book_obj1 = Registered_Books.objects.all().order_by(sort_by)
        union_queryset = book_obj1 
        return render(request,'manage-book.html',{"title":title,"books":union_queryset})


@login_required(login_url='http://127.0.0.1:8000/')  
def sortByRegisteredStudents(request):
    title = '''BBAU SATELLITE | Registered Students'''
    if request.method == 'POST':
        sort_by = request.POST.get('sort-by')
        print(sort_by)
        
        book_obj1 = Profile.objects.all().order_by(sort_by)
        return render(request,'registered-students.html',{"title":title,"books":book_obj1})
    

def issueBook(request):
    print(" in issue book funtion")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU SATELLITE | Issue Book'''

    try:
        if request.method == 'POST':
            print("posted")
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            print(ISBN,library_id)
            found = True
            book_obj = Registered_Books.objects.filter(ISBN = ISBN)
            profile_obj = Profile.objects.filter(library_id = library_id)
            print(profile_obj[0].issuedBooks)

            listOfIssueBooks = (profile_obj[0].issuedBooks).split()
            listOfReturnBooks = (profile_obj[0].returnedBooks).split()
            print(type(listOfIssueBooks),listOfIssueBooks,len(listOfIssueBooks))
            print(len(listOfIssueBooks),len(listOfReturnBooks))
            print(len(listOfIssueBooks) - len(listOfReturnBooks))
            
            # print(returned_obj.exists())
            if not book_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Book Not Found !!!")
                return render(request,'issue-book.html',{"title":title,"book":book_obj,"found":found})

            if not profile_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Student Not Found !!!")
                return render(request,'issue-book.html',{"title":title,"book":book_obj,"found":found})

            if (len(listOfIssueBooks) - len(listOfReturnBooks)) >= 2:
                found = False
                messages.add_message(request, messages.WARNING, "Already 2 Books Issued to this User !!!")
                return render(request,'issue-book.html',{"title":title,"book":book_obj,"student":profile_obj,"found":found})
            
            if not book_obj[0].status == "Available":
                found = False
                messages.add_message(request, messages.WARNING, "Record Not found for this details !!!")
                return render(request,'issue-book.html',{"title":title,"book":book_obj,"found":found})
            
            if profile_obj[0].issuedBooks == 'Null':
                profile_obj[0].issuedBooks = ""

            if profile_obj[0].returnedBooks == 'Null':
                profile_obj[0].returnedBooks = ""
            
            
            print(listOfIssueBooks,listOfReturnBooks)
            
            print(found)
            return render(request,'issue-book.html',{"title":title,"book":book_obj,"student":profile_obj,"IssuedBooks":len(listOfIssueBooks),"ReturnedBooks":len(listOfReturnBooks),"found":found})

    except Exception as e:
        print(e)
        return redirect('/')

    

def issuingBook(request):
    print(" in issuing book funtion")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    try:
        if request.method == 'POST':
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            book_obj = Registered_Books.objects.get(ISBN = ISBN)
            profile_obj = Profile.objects.get(library_id = library_id)   
            if profile_obj.issuedBooks == 'Null':
                profile_obj.issuedBooks = ""

            profile_obj.issuedBooks = profile_obj.issuedBooks + "{} ".format(ISBN)
            print(profile_obj.issuedBooks)
            profile_obj.save()
            book_obj.last_issued_by = profile_obj.name
            print(book_obj.status)
            book_obj.status = "Not Available"
            book_obj.save()
            print(book_obj.status)

            issued_book_obj = Issued_Books.objects.create(issued_by = profile_obj.name, email = profile_obj.user.email, mobile = profile_obj.mobile, issue_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN, category = book_obj.category )
            
            print(book_obj.status)
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
    title = '''BBAU SATELLITE | Issue Book'''

    try:
        if request.method == 'POST':
            print("posted")
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            print(ISBN,library_id)
            found = True
            book_obj = Registered_Books.objects.filter(ISBN = ISBN)
            profile_obj = Profile.objects.filter(library_id = library_id)
            issued_obj = Issued_Books.objects.filter(ISBN =ISBN,library_id = library_id)
            listOfIssueBooks = (profile_obj[0].issuedBooks).split()
            listOfReturnBooks = (profile_obj[0].returnedBooks).split()
            print(listOfIssueBooks,listOfReturnBooks)
            if not book_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Book Not Found !!!")

            if not profile_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Student Not Found !!!")

            if not issued_obj.exists():
                found = False
                messages.add_message(request, messages.WARNING, "Record Not found for this details !!!")
                return render(request,'return-book.html',{"title":title,"book":book_obj,"found":found})

            print(found)
            # return render(request,'return-book.html',{"title":title,"book":book_obj,"student":profile_obj,"found":found})
            return render(request,'return-book.html',{"title":title,"book":book_obj,"student":profile_obj,"IssuedBooks":len(listOfIssueBooks),"ReturnedBooks":len(listOfReturnBooks),"found":found})

    except Exception as e:
        print(e)
        return redirect('/')
    
    

def returningBook(request):
    print(" in returning book funtion")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    try:
        if request.method == 'POST':
            print("posted")
            ISBN = request.POST.get('ISBN')
            library_id = request.POST.get('library_id')
            fine = request.POST.get('fine')
            isPaid = request.POST.get('isPaid')
            print(fine,isPaid)
            book_obj = Registered_Books.objects.get(ISBN = ISBN)
            issued_books_obj = Issued_Books.objects.filter(ISBN = ISBN).last()
            profile_obj = Profile.objects.get(library_id = library_id)
            profile_obj.fine = profile_obj.fine + int(fine)
            issued_books_obj.return_date = timezone.now().strftime('%Y-%m-%d')
            if profile_obj.returnedBooks == 'Null':
                profile_obj.returnedBooks = ""
            profile_obj.returnedBooks = profile_obj.returnedBooks + "{} ".format(ISBN)
            print(book_obj.status)
            # Registered_Books.objects.update(last_issued_by = profile_obj.name, status = 'Available')
            book_obj.status = "Available"
            book_obj.last_returned_by = profile_obj.name
            print(book_obj.status)
            print(book_obj.last_returned_by)
            returned_books_obj = Returned_Books.objects.create(returned_by = profile_obj.name,issue_date = issued_books_obj.issue_date, email = profile_obj.user.email, fine = fine, isPaid = isPaid, mobile = profile_obj.mobile, return_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN, category = book_obj.category )

            book_obj.save()
            print(book_obj.status)
            profile_obj.save()
            issued_books_obj.save()
            returned_books_obj.save()
            return redirect('http://127.0.0.1:8000/returned-books/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.SUCCESS, "{}".format(e))
        return redirect('http://127.0.0.1:8000/')
    
def issuedBooks(request):
    print(" in issued book funtion")
    title = '''BBAU SATELLITE | Issued Books'''
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    

    if request.user.is_superuser:
        issued_book_obj = Issued_Books.objects.all()

    else:
        profil_obj = Profile.objects.filter(library_id = request.user.profile.library_id)
        listOfIssueBooks = (profil_obj[0].issuedBooks).split()
        issued_book_obj = Issued_Books.objects.filter(ISBN__in = listOfIssueBooks)

    
    return render(request,'issued-books.html',{"title":title,"issued_books":issued_book_obj})
    
def returnedBooks(request):
    print(" in returned book funtion")
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU SATELLITE | BBAU-LIBRARY | Returned Books'''
    
    if request.user.is_superuser:
        returned_books_obj = Returned_Books.objects.all()

    else:
        profil_obj = Profile.objects.filter(library_id = request.user.profile.library_id)
        listOfReturnBooks = (profil_obj[0].returnedBooks).split()
        returned_books_obj = Returned_Books.objects.filter(ISBN__in = listOfReturnBooks)

    return render(request,'returned-books.html',{"title":title,"returned_books":returned_books_obj})


def gallery(request):
    title = '''BBAU SATELLITE | Gallery'''
    return render(request,'gallery.html',{"title":title})

def contact(request):
    title = '''BBAU SATELLITE | Contact Us'''
    return render(request,'contact.html')
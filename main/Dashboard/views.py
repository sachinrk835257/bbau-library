from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books, Department
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from Authentication.send_mail import send_mail
from Authentication.models import ChangePassword
from tablib import Dataset
from Dashboard.resource import Registered_BooksResource,Returned_BooksResource,Issued_BooksResource,ProfileResource
from uuid import uuid4
from django.utils import timezone
from django.db.models import Count,Q
import pandas as pd

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
            authorName = request.POST.get('authorName')
            purchaseDate = request.POST.get('purchaseDate','Null')
            bookPrice = request.POST.get('bookPrice')
            billNo_Date = request.POST.get('billNo_Date','Null')
            place_and_publisher = request.POST.get('place_and_publisher','Null')
            edition = request.POST.get('edition','Null')
            volume = request.POST.get('volume','Null')
            printYear = request.POST.get('printYear','Null')       
            bookPages = request.POST.get('bookPages','Null')
            bookContact = request.POST.get('bookContact','Null')
            bookSource = request.POST.get('bookSource','Null')
            withDrawDate = request.POST.get('withDrawDate','Null')
            if (" " in isbn or "," in isbn):
                messages.add_message(request, messages.WARNING, "ISBN without characters of \'  \', or \' , \' !!!")
                return redirect('http://127.0.0.1:8000/add-book/')


            # print(bookName,department,isbn,authorName,bookPrice,purchaseDate,place_and_publisher,withDrawDate,volume,edition,bookSource,bookContact,printYear,billNo_Date,coverImage,sep=", ")  
            try:

                if request.FILES:
                    coverImage = request.FILES['coverImage']
                    if not (coverImage.name.endswith('jpeg') or coverImage.name.endswith('jpg')):
                        messages.add_message(request, messages.WARNING, "Please upload .jpeg or .jpg image only !!!")
                        return redirect('http://127.0.0.1:8000/add-book/')
                    # print(bookName,department,isbn,authorName,bookPrice,coverImage)    
                    book_obj = Registered_Books.objects.create(register_by = f"{request.user.first_name} {request.user.last_name}", purchaseDate = purchaseDate,ISBN = isbn,authorName = authorName,bookName = bookName,department = department,edition = edition,place_and_publisher = place_and_publisher,printYear = printYear,bookPages = bookPages,volume = volume,bookSource = bookSource,bookPrice = bookPrice,bookContact = bookContact,billNo_Date = billNo_Date,withDrawDate = withDrawDate,coverImage = coverImage)

                else:
                    book_obj = Registered_Books.objects.create(register_by = f"{request.user.first_name} {request.user.last_name}", purchaseDate = purchaseDate,ISBN = isbn,authorName = authorName,bookName = bookName,department = department,edition = edition,place_and_publisher = place_and_publisher,printYear = printYear,bookPages = bookPages,volume = volume,bookSource = bookSource,bookPrice = bookPrice,bookContact = bookContact,billNo_Date = billNo_Date,withDrawDate = withDrawDate)

                book_obj.save()
                messages.add_message(request, messages.SUCCESS, "Book Added Successfully")
                return redirect('http://127.0.0.1:8000/manage-book/')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.WARNING, "Technical Error !!!")
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
            authorName = request.POST.get('authorName')
            purchaseDate = request.POST.get('purchaseDate','Null')
            bookPrice = request.POST.get('bookPrice')
            billNo_Date = request.POST.get('billNo_Date','Null')
            place_and_publisher = request.POST.get('place_and_publisher','Null')
            edition = request.POST.get('edition','Null')
            volume = request.POST.get('volume','Null')
            printYear = request.POST.get('printYear','Null')
            bookPages = request.POST.get('bookPages','Null')
            bookContact = request.POST.get('bookContact','Null')
            bookSource = request.POST.get('bookSource','Null')
            withDrawDate = request.POST.get('withDrawDate','Null')
        
            if "," in isbn:
                isbn = ''.join(isbn.split())
                isbn = isbn.split(',')
                print(isbn)
            else:
                messages.add_message(request, messages.WARNING, "unique ISBN should be written with comma seperated  !!!")
                return redirect('http://127.0.0.1:8000/multiple-entry/')
            
            print(bookName,department,isbn,authorName,bookPrice,purchaseDate,place_and_publisher,withDrawDate,volume,edition,bookSource,bookContact,printYear,billNo_Date,sep=", ") 
            print(request.FILES) 
            try:
                if request.FILES:
                    coverImage = request.FILES['coverImage']
                    if not (coverImage.name.endswith('jpeg') or coverImage.name.endswith('jpg')):
                        messages.add_message(request, messages.WARNING, "Please upload .jpeg or .jpg image only !!!")
                        return redirect('http://127.0.0.1:8000/multiple-entry/')
                    for i in isbn:
                        book_obj = Registered_Books.objects.create(register_by = f"{request.user.first_name} {request.user.last_name}", purchaseDate = purchaseDate,ISBN = i,authorName = authorName,bookName = bookName,department = department,edition = edition,place_and_publisher = place_and_publisher,printYear = printYear,bookPages = bookPages,volume = volume,bookSource = bookSource,bookPrice = bookPrice,bookContact = bookContact,billNo_Date = billNo_Date,withDrawDate = withDrawDate,coverImage = coverImage)
                else:  
                    for j in isbn:
                        book_obj = Registered_Books.objects.create(register_by = f"{request.user.first_name} {request.user.last_name}", purchaseDate = purchaseDate,ISBN = j,authorName = authorName,bookName = bookName,department = department,edition = edition,place_and_publisher = place_and_publisher,printYear = printYear,bookPages = bookPages,volume = volume,bookSource = bookSource,bookPrice = bookPrice,bookContact = bookContact,billNo_Date = billNo_Date,withDrawDate = withDrawDate)
            except Exception as e:
                print(e)
                messages.add_message(request, messages.WARNING, "Technical Error !!!")
                return redirect('http://127.0.0.1:8000/multiple-entry/')
            
            book_obj.save()
            messages.add_message(request, messages.SUCCESS, f"Books {isbn} Added Successfully")
            return redirect('http://127.0.0.1:8000/manage-book/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "ISBN should be Unique OR Technical Error !!!")
        return redirect('http://127.0.0.1:8000/multiple-entry/')
    
    return render(request,'add-same-book.html',{"title":title,"Departments":department_obj})


def importFile(request):
    print("in import Book")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    title = '''BBAU SATELLITE | Import Excel File'''
    try:
        if request.method == 'POST':
            print("posted")
            dateset = Dataset()
            print("next")
            myfile = request.FILES.get('myfile')
            print(myfile)
            if not myfile.name.endswith('xlsx'):
                messages.add_message(request, messages.WARNING, "WRONG FILE FORMAT !!!")
                return redirect('http://127.0.0.1:8000/import-file/')
            imported_data = dateset.load(myfile.read(),format="xlsx")

            for data in imported_data:
                # DATE Accession Number AUTHOR TITLE Deparmtent Edition Place&Publishers Year Pages. Vol. Source Cost Call No.	Bill No.&Date  WithdrawlDate & Rem.		
                # print(data)
                # print(data[0],"--",data[1],"---",data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[15])
                try:
                    register_obj = Registered_Books.objects.create(register_by = f"{request.user.first_name} {request.user.last_name}", purchaseDate = data[0],ISBN = data[1],authorName = data[2],bookName = data[3],department = data[4],edition = data[5],place_and_publisher = data[6],printYear = data[7],bookPages = data[8],volume = data[9],bookSource = data[10],bookPrice = data[11],bookContact = data[12],billNo_Date = data[13],withDrawDate = data[14])
                    
                except Exception as e:
                    print(e)
                    messages.add_message(request, messages.WARNING, "{}".format(e))
                    return redirect('http://127.0.0.1:8000/import-file/')
            register_obj.save()
            messages.add_message(request, messages.SUCCESS, "Book Added Successfully")
            return redirect('http://127.0.0.1:8000/manage-book/')


    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "ISBN should be Unique OR Technical Error !!!")
        return redirect('http://127.0.0.1:8000/import-file/')
    
    
    return render(request,'import-file.html',{"title":title,})

def exportFile(request):
    print("export Book")
    # if not request.user.is_superuser:
    #     messages.add_message(request, messages.WARNING, "Admin Login First !!!")
    #     return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    # title = '''BBAU SATELLITE | Export File'''
    # department_obj = Department.objects.all()
    try:
        # if request.method == 'POST':
        #     print("posted")
        books = Registered_Books.objects.all()
        data = []
        for obj in books:
            count = 1
            data.append({"Sr No.":count,"Book Name":obj.bookName,"Register By":obj.register_by,"Department":obj.department,"Author Name":obj.authorName,"Book ISBN":obj.ISBN,"Book Price":obj.bookPrice,"Registered Date":obj.registered_at.date()})
            count += 1
            print(count)
        print(pd.DataFrame(data).to_excel("Book_Details.xlsx"))
        print(data)
        return redirect('http://127.0.0.1:8000/')

    except Exception as e:
        print(e)
        messages.add_message(request, messages.WARNING, "{}".format(e))
        return redirect('http://127.0.0.1:8000/add-book/')
    
    return render(request,'export-file.html',{"title":title,"Departments":department_obj})

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
        # print(book_obj.count())
        same_books = book_obj.values('bookName','authorName','department').annotate(book_count = Count("pk"), availability_count=Count('id', filter=Q(status='Available')),
        not_availability_count=Count('id', filter=Q(status='Not Available'))).filter(book_count__gt=1)
        # print(same_books,type(same_books))
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
    print("in book details")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    
    title = '''BBAU SATELLITE | Update Books Details'''
    departments = Department.objects.all()
    book_obj1 = Registered_Books.objects.get(ISBN = isbn)
    
    return render(request,'book-detail.html', {"title":title,"book":book_obj1,"Departments":departments})

def updateBook(request,isbn):
    print("in update")
    if not request.user.is_superuser:
        messages.add_message(request, messages.WARNING, "Admin Login First !!!")
        return redirect('http://127.0.0.1:8000/authenticate/admin-login/')
    if request.method == 'POST':
        print("posted")
        try:
            book_obj1 = Registered_Books.objects.get(ISBN = isbn)     
            bookName = request.POST.get('bookName')
            department = request.POST.get('department')
            authorName = request.POST.get('authorName')
            purchaseDate = request.POST.get('purchaseDate','Null')
            bookPrice = request.POST.get('bookPrice')
            billNo_Date = request.POST.get('billNo_Date','Null')
            place_and_publisher = request.POST.get('place_and_publisher','Null')
            edition = request.POST.get('edition','Null')
            volume = request.POST.get('volume','Null')
            printYear = request.POST.get('printYear','Null')
            bookPages = request.POST.get('bookPages','Null')
            bookContact = request.POST.get('bookContact','Null')
            bookSource = request.POST.get('bookSource','Null')
            withDrawDate = request.POST.get('withDrawDate','Null')
            book_obj1.bookName = bookName
            book_obj1.authorName = authorName
            book_obj1.department = department
            book_obj1.bookPrice = bookPrice
            book_obj1.purchaseDate = purchaseDate
            book_obj1.billNo_Date = billNo_Date
            book_obj1.place_and_publisher = place_and_publisher
            book_obj1.volume = volume
            book_obj1.edition = edition
            book_obj1.printYear = printYear
            book_obj1.bookPages = bookPages
            book_obj1.bookContact = bookContact
            book_obj1.bookSource = bookSource
            book_obj1.withDrawDate = withDrawDate
            print("done")
            print(bookName,department,isbn,authorName,bookPrice,purchaseDate,place_and_publisher,withDrawDate,volume,edition,bookSource,bookContact,printYear,billNo_Date,sep=", ")  
        except Exception as e:
            print(e)
            messages.add_message(request, messages.WARNING, "Technical Error !!!")
            return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))
        try:
            if request.FILES :
                coverImage = request.FILES['coverImage']
                # print(coverImage)
                if coverImage:
                    if not(coverImage.name.endswith('jpg') or coverImage.name.endswith('jpeg')):
                        # print("in this")
                        messages.add_message(request, messages.WARNING, "Upload jpeg or jpg image file only !!!")
                        return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))
                    book_obj1.coverImage = coverImage

        except:
            messages.add_message(request, messages.WARNING, "Image Uploading Error !!!")
            return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))

        book_obj1.save()
        messages.add_message(request, messages.SUCCESS, "Book Updated Successfully")
        return redirect('http://127.0.0.1:8000/edit-book/{}'.format(isbn))

@login_required(login_url='http://127.0.0.1:8000/')
def searchByRegisteredBooks(request):
    title = '''BBAU SATELLITE | Registered Books'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by').upper()
        print(search)
        book_obj1 = Registered_Books.objects.filter(bookName__contains = search)
        book_obj2 = Registered_Books.objects.filter(ISBN__contains = search)
        book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        book_obj4 = Registered_Books.objects.filter(department__contains = search)
        book_obj5 = Registered_Books.objects.filter(status__contains = search)
        union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5
        print(union_queryset)

        return render(request,'searched.html',{"title":title,"books":union_queryset})
    
@login_required(login_url='http://127.0.0.1:8000/')
def searchByManageBooks(request):
    title = '''BBAU SATELLITE | Manage Books'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by').upper()
        print(search)
        book_obj1 = Registered_Books.objects.filter(bookName__contains = search)
        book_obj2 = Registered_Books.objects.filter(ISBN = search)
        book_obj3 = Registered_Books.objects.filter(authorName__contains = search)
        book_obj4 = Registered_Books.objects.filter(department__contains = search)
        book_obj5 = Registered_Books.objects.filter(status__contains = search)
        union_queryset = book_obj1 | book_obj2 | book_obj3 | book_obj4 | book_obj5
        print(union_queryset)

        return render(request,'searched-books-table.html',{"title":title,"books":union_queryset})

@login_required(login_url='http://127.0.0.1:8000/')
def searchByRegisteredStudents(request):
    title = '''BBAU SATELLITE | Registered Students'''
    if request.method == 'POST':
        print(request)
        search = request.POST.get('search-by').upper()
        print(search)
        book_obj1 = Profile.objects.filter(name__contains = search)
        book_obj2 = Profile.objects.filter(library_id = search)
        book_obj4 = Profile.objects.filter(department__contains = search)
        union_queryset = book_obj1 | book_obj2 | book_obj4 
        print(union_queryset)

        return render(request,'searched-students-table.html',{"title":title,"students":union_queryset})

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
            print(book_obj,profile_obj)

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

            issued_book_obj = Issued_Books.objects.create(issued_by = profile_obj.name, email = profile_obj.user.email, mobile = profile_obj.mobile, issue_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN)
            
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
            returned_books_obj = Returned_Books.objects.create(returned_by = profile_obj.name,issue_date = issued_books_obj.issue_date, email = profile_obj.user.email, fine = fine, isPaid = isPaid, mobile = profile_obj.mobile, return_date = timezone.now().strftime('%Y-%m-%d'),library_id = profile_obj.library_id,bookName = book_obj.bookName, authorName = book_obj.authorName, department = book_obj.department, ISBN = book_obj.ISBN)

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
from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# Create your models here.
GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('OTHER', 'Other'),
)

class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    name = models.CharField(default="",max_length=30,verbose_name="STUDENT NAME")
    semester = models.CharField(default="",max_length=10,verbose_name="Semester")
    gender = models.CharField(default="MALE",max_length=6, choices=GENDER_CHOICES)
    department = models.CharField(default="",max_length=50,verbose_name="DEPARTMENT")
    library_id = models.CharField(default="",unique=True, max_length=10,verbose_name="LIBRARY ID")
    mobile = models.CharField(default="", max_length=10,verbose_name="MOBILE NO.")
    joiningYear = models.CharField(default="",max_length=4,verbose_name="ADMISSION YEAR")
    passingYear = models.CharField(default="",max_length=4,verbose_name="PASSING YEAR")
    issuedBooks = models.TextField(default="Null",verbose_name="ISSUED BOOKS")
    returnedBooks = models.TextField(default="Null",verbose_name="RETURNED BOOKS")
        
    def __str__(self) -> str:
        return self.user.username
    
class Registered_Books(models.Model):
    # book columns
    bookName = models.CharField(default="",max_length=255, verbose_name="Book Name")
    department = models.CharField(default="Null",null = True,max_length=50, verbose_name="Department")
    # category = models.CharField(default="Null",max_length=50, verbose_name="Category")
    ISBN = models.CharField(default="",unique=True,max_length=255, verbose_name="ISBN Number")
    authorName = models.CharField(default="",max_length=50, verbose_name="Author Name")
    purchaseDate = models.TextField(default = "00-00-0000", max_length = 15,verbose_name="Purchase Date")
    bookPrice = models.CharField(default="Null",null = True,max_length=20, verbose_name="Book Price")
    billNo_Date = models.TextField(default="Not Available",blank = False, verbose_name="Bill No and Date")
    place_and_publisher = models.TextField(default = "Null",null = True, verbose_name ="Place And Publisher")
    edition = models.CharField(default = "Null",null = True,max_length = 10,verbose_name ="Edition")
    volume = models.CharField(default="Null",null = True,max_length = 10,verbose_name = "Volume")
    printYear = models.CharField(default = "Null",null = True,max_length = 10, verbose_name = "Printed Year")
    bookPages = models.CharField(default = "Null",null = True, max_length = 30, verbose_name = "Book Pages")
    bookContact = models.TextField(default = "Null",null = True, verbose_name ="Call No.")
    bookSource = models.TextField(default="Not Available", verbose_name="Book Source")
    withDrawDate = models.TextField(default = "Null",null = True, verbose_name ="WithDraw Date & Remarks")
    # self created columns
    register_by = models.CharField(default="",max_length=50, verbose_name="book register by")
    coverImage = models.ImageField(default = "",upload_to='cover images/',verbose_name="Book Cover Image")
    status = models.CharField(default="Available",max_length=30,verbose_name="Status")
    last_issued_by = models.CharField(default="null",null=True, max_length=30,verbose_name="Last Issued By")
    last_returned_by = models.CharField(default="null",null=True, max_length=30,verbose_name="Last Returned By")
    registered_at = models.DateTimeField(auto_now_add=True,verbose_name="Registered At")

    def __str__(self) -> str:
        return self.bookName + " " + self.ISBN

class Issued_Books(models.Model):
    issued_by = models.CharField(default="Null",max_length=30,verbose_name="Issued By")
    department = models.CharField(default="",max_length=50, verbose_name="Department")
    semester = models.CharField(default="",max_length=10,verbose_name="Semester")
    email = models.EmailField(default="",max_length=50, verbose_name="Email")
    mobile = models.PositiveIntegerField(verbose_name="Mobile Number")
    status = models.CharField(default="Issued",max_length=30,verbose_name="Status")
    issue_date = models.CharField(default="Null",max_length=15,verbose_name="Issue Date")
    return_date = models.CharField(default="Null",max_length=15,verbose_name="Return Date")
    library_id = models.CharField(default="", max_length=10,verbose_name="Library ID")
    bookName = models.CharField(default="",max_length=255, verbose_name="Book Name")
    # category = models.CharField(default="",max_length=50, verbose_name="Category")
    authorName = models.CharField(default="",max_length=50, verbose_name="Author Name")
    ISBN = models.CharField(default="",max_length=255, verbose_name="ISBN Number")

    def __str__(self) -> str:
        return self.library_id + self.bookName + self.ISBN

class Returned_Books(models.Model):
    returned_by = models.CharField(default="Null",max_length=30,verbose_name="Returned By")
    email = models.EmailField(default="",max_length=50, verbose_name="Email")
    mobile = models.PositiveIntegerField(verbose_name="Mobile Number")
    issue_date = models.CharField(default="Null",max_length=15,verbose_name="Issue Date")
    return_date = models.CharField(default="Null", max_length=15,verbose_name="Return Date")
    library_id = models.CharField(default="", max_length=10,verbose_name="Library ID")
    bookName = models.CharField(default="",max_length=255, verbose_name="Book Name")
    fine = models.PositiveIntegerField(default=0,verbose_name="FINE (in RS.)")
    # isPaid = models.BooleanField(default=False,null=False)
    std_department = models.CharField(default="",max_length=50, verbose_name=" Student Department")
    semester = models.CharField(default="",max_length=10,verbose_name="Semester")
    # category = models.CharField(default="",max_length=50, verbose_name="Category")
    authorName = models.CharField(default="",max_length=50, verbose_name="Author Name")
    ISBN = models.CharField(default="",max_length=255, verbose_name="ISBN Number")

    def __str__(self) -> str:
        return self.library_id + self.bookName + self.ISBN


class Department(models.Model):
    departmentName = models.CharField(default="Null",max_length=50,verbose_name="Department Name")

    def __str__(self) -> str:
        return self.departmentName

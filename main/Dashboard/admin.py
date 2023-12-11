from django.contrib import admin
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books, Department
from import_export.admin import ImportExportModelAdmin


# admmin model
@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('library_id','name', 'department','mobile')
    list_filter = ('name','mobile')
    search_fields = ('name', 'department')


@admin.register(Registered_Books)
class Registered_BooksAdmin(ImportExportModelAdmin):
    list_display = ('register_by','bookName', 'ISBN', 'department','status','authorName','coverImage')
    list_filter = ('bookName','authorName','ISBN','department')
    search_fields = ('bookName', 'department','ISBN','authorName')

@admin.register(Returned_Books)
class Returned_BooksAdmin(ImportExportModelAdmin):
    list_display = ('library_id','returned_by','bookName','ISBN', 'department','authorName')
    list_filter = ('library_id','returned_by','bookName','ISBN', 'department','authorName')
    search_fields = ('library_id','returned_by','bookName','ISBN', 'department','authorName')

@admin.register(Issued_Books)
class Issued_BooksAdmin(ImportExportModelAdmin):
    list_display = ('library_id','issued_by','bookName','ISBN', 'department','authorName')
    list_filter = ('library_id','issued_by','bookName','ISBN', 'department','authorName')
    search_fields = ('library_id','issued_by','bookName','ISBN', 'department','authorName')

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('departmentName',)



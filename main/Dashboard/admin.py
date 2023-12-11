from django.contrib import admin
from Dashboard.models import Profile,Registered_Books,Issued_Books,Returned_Books, Department

# admmin model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('library_id','name', 'department','mobile')
    list_filter = ('name','mobile')
    search_fields = ('name', 'department')

class Registered_Books_Admin(admin.ModelAdmin):
    list_display = ('register_by','bookName', 'ISBN', 'department','status','authorName','coverImage')
    list_filter = ('bookName','authorName','ISBN','department')
    search_fields = ('bookName', 'department','ISBN','authorName')
    
class Issued_Books_Admin(admin.ModelAdmin):
    list_display = ('library_id','issued_by','bookName','ISBN', 'department','authorName')
    list_filter = ('library_id','issued_by','bookName','ISBN', 'department','authorName')
    search_fields = ('library_id','issued_by','bookName','ISBN', 'department','authorName')

class Returned_Books_Admin(admin.ModelAdmin):
    list_display = ('library_id','returned_by','bookName', 'ISBN', 'department','authorName')
    list_filter = ('library_id','returned_by','bookName','ISBN', 'department','authorName')
    search_fields = ('library_id','returned_by','bookName','ISBN', 'department','authorName')
# Register your models here.

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Registered_Books,Registered_Books_Admin)
admin.site.register(Issued_Books,Issued_Books_Admin)
admin.site.register(Returned_Books,Returned_Books_Admin)
admin.site.register(Department)

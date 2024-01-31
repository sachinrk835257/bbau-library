from django.contrib import admin
from Authentication.models import ChangePassword,SuperUserReference

# Register your models here.
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at','token')
admin.site.register(ChangePassword)
admin.site.register(SuperUserReference,SuperUserAdmin)


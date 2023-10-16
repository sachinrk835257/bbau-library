from django.contrib import admin
from Authentication.models import ChangePassword,SuperUser

# Register your models here.
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('id','name','user')
admin.site.register(ChangePassword)
admin.site.register(SuperUser,SuperUserAdmin)


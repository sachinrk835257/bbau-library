
from django.urls import path,include
# from  django.conf import settings
from Authentication import views
from Dashboard import views

urlpatterns = [
    path('',views.index, name="home page"),
    path('register/',views.register, name="go to register"),
    path('adminLogin/',views.adminLogin, name="go to admin login"),
    path('dashboard/',views.dashboard, name="go to dashboard login"),
    path('registered-students/',views.regStudents, name="go to registered students"),
    path('edit-profile/',views.editProfile, name="go to edit student profile"),
    path('delete-profile/<int:myid>',views.delprofile, name="go to delete student"),
    path('authenticate/',include('Authentication.urls'),name="go to authentication")    
] 
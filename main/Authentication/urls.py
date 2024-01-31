from django.urls import path
# from  django.conf import settings
from Authentication import views

urlpatterns = [
    path('register/',views.addStudent, name="register page"),
    path('login/',views.user_login, name="login page"), 
    path('create-admin/',views.adminRegister, name="admin register page"), 
    path('admin-login/',views.admin_login, name="admin page"), 
    path('admin-password/<str:passToken>/',views.setPassword, name="Set Password"), 
    path('change-password/<uuid:token>/',views.forgotChangePassword, name="change password"), 
    path('change-password/<int:id>',views.changePassword, name="change password"), 
    path('logout/',views.logout_page, name="logout page"),    
]
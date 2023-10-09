from django.urls import path
# from  django.conf import settings
from Authentication import views


urlpatterns = [
    path('login/',views.login_page, name="home page"), 
    path('register/',views.register, name="register page"), 
    path('logout/',views.logout_page, name="logout page"),    
] 
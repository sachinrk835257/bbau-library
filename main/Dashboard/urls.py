
from django.urls import path,include
# from  django.conf import settings
from Authentication import views
from Dashboard import views

urlpatterns = [
    path('',views.index, name="home page"),
    # path('dashboard/',views.dashboard, name="go to dashboard login"),
    path('registered-students/',views.regStudents, name="go to registered students"),
    path('edit-profile/<int:myid>/',views.editProfile, name="go to edit student profile"),
    path('listed-books/',views.listedBooks, name="go to registered books"),
    path('edit-book/<str:isbn>/',views.bookDetails, name="go to specific book detail"),
    path('delete-book/<str:isbn>/',views.deleteBook, name="go to specific book detail"),
    path('delete-profile/<int:myid>/',views.deleteProfile, name="see profile of student"),
    path('add-book/',views.addBook, name="add book"),
    path('manage-book/',views.manageBook, name="manage book"),
    path('search-by/',views.searchBy, name="search book"),
    path('sort-by/',views.applyFilter, name="sorting of books"),
    path('forgot-password/',views.forgotPassword, name="forgot passwordt"),
    path('authenticate/',include('Authentication.urls'),name="go to authentication")    

]
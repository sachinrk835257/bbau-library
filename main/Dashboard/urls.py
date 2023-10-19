
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
    path('issue-book/',views.issueBook, name="issue book"),
    path('issuing-book/',views.issuingBook, name="issue book"),
    path('return-book/',views.returnBook, name="return book"),
    path('returning-book/',views.returningBook, name="issue book"),
    path('manage-book/',views.manageBook, name="manage book"),
    
    path('registered-books-search-by/',views.searchByRegisteredBooks, name="search book"),
    path('manage-books-search-by/',views.searchByManageBooks, name="search book"),
    path('registered-students-search-by/',views.searchByRegisteredStudents, name="search book"),
    path('registered-students-sort-by/',views.sortByRegisteredStudents, name="search book"),
    path('manage-books-sort-by/',views.sortByManageBooks, name="sorting of books"),
    path('registered-books-sort-by/',views.sortByRegisteredBooks, name="sorting of books"),
    
    path('issued-books/',views.issuedBooks, name="issued books"),
    path('returned-books/',views.returnedBooks, name="returned books"),
    path('forgot-password/',views.forgotPassword, name="forgot passwordt"),
    path('authenticate/',include('Authentication.urls'),name="go to authentication")    

]
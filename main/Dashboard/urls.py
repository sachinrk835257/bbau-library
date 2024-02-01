
from django.urls import path, include
# from  django.conf import settings
from Authentication import views
from Dashboard import views

urlpatterns = [
    path('',views.index, name="home page"),
    # path('dashboard/',views.dashboard, name="go to dashboard login"),

    path('authenticate/',include('Authentication.urls'),name="go to authentication") ,

    path('registered-students/',views.regStudents, name="go to registered students"),
    path('about/',views.about, name="go to registered students"),
    path('user-login/',views.userLogin, name="go to login page"),
    path('gallery/',views.gallery, name="gallery"),
    path('edit-profile/<int:myid>/',views.editProfile, name="go to edit student profile"),
    path('listed-books/',views.listedBooks, name="go to registered books"),
    path('edit-book/<str:isbn>/',views.bookDetails, name="go to specific book detail"),
    path('update-book/<str:isbn>/',views.updateBook, name="update book detail"),
    path('delete-book/<str:isbn>/',views.deleteBook, name="go to specific book detail"),
    path('delete-profile/<int:myid>/',views.deleteProfile, name="see profile of student"),
    path('add-book/',views.addBook, name="add book"),
    path('multiple-entry/',views.addMultiple, name="add Multiple book"),
    path('import-file/',views.importFile, name="add book"),
    path('export-file/',views.exportFile, name="add Multiple book"),
    path('issue-book/',views.issueBook, name="issue book"),
    path('issuing-book/',views.issuingBook, name="issue book"),
    path('return-book/',views.returnBook, name="return book"),
    path('returning-book/',views.returningBook, name="issue book"),
    path('manage-book/',views.manageBook, name="manage book"),
    
    path('registered-books-search-by/',views.searchByRegisteredBooks, name="search book"),
    path('manage-books-search-by/',views.searchByManageBooks, name="search book"),
    path('registered-students-search-by/',views.searchByRegisteredStudents, name="search book"),
    path('contact-us/',views.contact, name="go to contact"),
    
    path('issued-books/',views.issuedBooks, name="issued books"),
    path('returned-books/',views.returnedBooks, name="returned books"),
    
    path('forgot-password/',views.forgotPassword, name="forgot passwordt"),

]
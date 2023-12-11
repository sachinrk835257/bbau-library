from .models import Registered_Books,Returned_Books,Issued_Books,Profile
from import_export import resources
from Dashboard.models import Profile

class ProfileResource(resources.ModelResource):
    class meta:
        model = Profile

class Registered_BooksResource(resources.ModelResource):
    class meta:
        model = Registered_Books

class Returned_BooksResource(resources.ModelResource):
    class meta:
        model = Returned_Books

class Issued_BooksResource(resources.ModelResource):
    class meta:
        model = Issued_Books
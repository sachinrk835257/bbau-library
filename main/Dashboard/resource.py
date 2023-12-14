from .models import Registered_Books,Returned_Books,Issued_Books,Profile
from import_export import resources,fields,widgets
from Dashboard.models import Profile
from django.contrib.auth.models import User

class ProfileResource(resources.ModelResource):
    user = fields.Field(column_name='user', attribute='email')
    print(user,widgets.ForeignKeyWidget(User, 'email'))
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
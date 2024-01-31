from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SuperUserReference(models.Model):
    # user = models.OneToOneField(User,related_name="admin",on_delete=models.CASCADE)
    name = models.CharField(default="",max_length=30)
    libraryId = models.CharField(default="",max_length=30)
    email = models.EmailField(default="",max_length=20)
    reference_by = models.CharField(default="",max_length=20)
    gender = models.CharField(default="MALE",max_length=6)
    mobile = models.CharField(max_length=10,default="")
    token = models.CharField(default = "Error", max_length = 50, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email + " {}".format(self.created_at) 

class ChangePassword(models.Model):
    token = models.CharField(default="",max_length=50)
    email = models.EmailField(default="",max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.email + " {}".format(self.timestamp)

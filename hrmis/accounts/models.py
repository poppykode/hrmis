from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User (AbstractUser):
    DES = (('', 'Choose Designation'), ('admin', 'Admin(Organization)'),('employee', 'Employee'),)
    GENDER = (('', 'Choose Gender'),('female','Female'),('male','Male'))
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    designation = models.CharField(max_length=30, choices=DES)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=50, choices=GENDER)
    address = models.TextField()

    def __str__(self):
        return self.first_name.capitalize() + ' ' + self.last_name.capitalize() +' ('+(self.username)+')'

    class Meta:
        ordering = ["-date_joined", ]
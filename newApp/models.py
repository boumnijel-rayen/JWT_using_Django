from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Admin(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'admin'

class employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.IntegerField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'employee'


    def __str__(self):
        return self.name

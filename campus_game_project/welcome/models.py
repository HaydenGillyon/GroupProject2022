from email.policy import default
from django.db import models


# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=40)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    points = models.PositiveIntegerField(default=0, null=True)
    profile = models.CharField(max_length=50, default='home/zombie.png')
    

class Admin(models.Model):

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

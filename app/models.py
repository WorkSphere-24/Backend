from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from .manager import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# maangers
# class CustomManager(models.Manager):
#     def get_queryset(self) :
#         return super().get_queryset().order_by('name')

# # Create your models here.
# class Student(models.Model):
#     user=models.ManyToManyField(User)
#     name = models.CharField(max_length=70)
#     roll = models.IntegerField()
#     #students=models.Manager()
#     students=CustomManager

#     def division(self):
#         return ','.join([str(p) for p in self.user.all()])



class CustomUser(AbstractUser):
    username = None
    name=models.CharField(max_length=70)
    email=models.EmailField(_("email address"),unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name


class user(models.Model):
    user1=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='user1')

class Status(models.Model):
    task_status = models.CharField(max_length=70,unique=True)

    def __str__(self):
        return self.task_status


class Priority(models.Model):
    priority_status = models.CharField(max_length=70,unique=True)

    def __str__(self):
        return self.priority_status
    
class Team(models.Model):
    members = models.ManyToManyField(CustomUser,related_name='members')
    def team_members(self):
        return ",".join([str(p) for p in self.members.all()])
    
    def add_member(self,user):
        self.members.add(user)

    def remove_member(self,user):
        self.members.remove(user)
    
    def __str__(self):
        return str(self.id)

class Chat(models.Model):
    content = models.CharField(max_length=100)
    timestamp =  models.DateTimeField(auto_now=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,null = True)

class Task(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE,null=True)
    notes = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    team = models.ForeignKey(Team,on_delete= models.CASCADE,null = True)
    files = models.FileField(upload_to="tasks/",max_length=255,null=True,default=None,blank=True)

    def __str__(self):
        return self.task
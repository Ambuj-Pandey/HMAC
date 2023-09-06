from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username ,password, is_active=True, is_staff=False, is_superuser=False, full_name=None):

        if not email:
            raise ValueError('Invalid Email')

        if not password:
            raise ValueError('Password cannot be empty')


        User = self.model(
            email=self.normalize_email(email)
        )
        User.username = username
        User.is_active = is_active
        User.is_staff = is_staff
        User.is_superuser = is_superuser

        User.set_password(password)
       
        User.full_name=full_name

        User.save(using=self.db)
        return User

    def create_staffuser(self, email, username, password):
        User = self.create_user(
            email=email,
            username=username,
            password=password, 
            is_staff=True,
            is_superuser=False
            )
        return User


    def create_superuser(self, email, username, password):
        User = self.create_user(
            email=email,
            username=username,
            password=password,
            is_staff=True, 
            is_superuser=True
            )
        return User
    

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    full_name = models.CharField(max_length=50, null=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

import datetime
import os
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime('%Y%m%d%X')
    new_filename = "{}{}".format(now_time,filename)
    return os.path.join('media/',new_filename)


class AdminLoginManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        # User creation logic
        if not email:
            raise ValueError('User must have an email.')
        if not username:
            raise ValueError('User must have a username.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        # Superuser creation logic
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AdminLogin(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.CharField(max_length=150, unique=True, blank=False)
    password = models.CharField()
    ph_no = PhoneNumberField(region='US', unique=True, blank=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AdminLoginManager()


class courses(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Technologies = models.CharField(max_length=150)
    Images = models.ImageField(upload_to= getFileName, blank=False)
    STATUS_CHOICES = (
    (0, 'enabled'),
    (1, 'disabled'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

class technologies(models.Model):
    Technologies = models.CharField(max_length=150)
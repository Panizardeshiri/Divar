from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_({'detail': "This Field is requred!"} ))
        username = self.normalize_email(username)
        user = self.model(username=username, email=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        return self.create_user(username, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length=255, unique=True)
    email           = models.EmailField(max_length=255, blank=True, null=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=5,default=0)
    forget_code = models.CharField(max_length=5,default=0)
    stars = models.CharField(max_length=2,blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __str__(self):
        return self.username
    


# class YourModel(models.Model):
#     name = models.CharField(max_length=100)
#     data = models.JSONField()


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """User Manager"""
    
    def create_user(self, email, password=None, **kwargs):
        """Creates and saves user"""
        
        if not email:
            raise ValueError('Email is provided.')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        """Creates superuser"""
        
        user = self.create_user(email=email, password=password, **kwargs)
        
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
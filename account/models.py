from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, email=None, username=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = self.model(phone_number=phone_number, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=False, null=True)
    username = models.CharField(max_length=150, blank=False, null=True)
    data_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

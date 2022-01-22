from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class HotelManager(BaseUserManager):
    def create_user(self, name, description, email, contact, username, password=None):
        hotel_user = self.model(
            name=name,
            description=description,
            email=self.normalize_email(email),
            contact=contact,
            username=username,
        )
        hotel_user.set_password(password)
        hotel_user.save()

        return hotel_user

    def create_superuser(self, name, description, email, contact, username, password):
        hotel_user = self.create_user(
            name=name,
            description=description,
            email=self.normalize_email(email),
            contact=contact,
            username=username,
            password=password,
        )
        hotel_user.is_admin=True
        hotel_user.is_staff=True
        hotel_user.is_superuser=True
        hotel_user.save()

        return hotel_user

class Hotel(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=10)
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name', 'description', 'email', 'contact']

    objects = HotelManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
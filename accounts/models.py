from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class UserType(models.Model):
    HOTEL = 1
    ROOM_MANAGER = 2
    CUSTOMER = 3
    CHOICES = (
        (HOTEL, 'Hotel'),
        (ROOM_MANAGER, 'Room Manager'),
        (CUSTOMER, 'Customer'),
    )

    id = models.PositiveSmallIntegerField(choices=CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_hotel = models.BooleanField(default=False)
    is_room_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    usertype = models.ManyToManyField(UserType)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True


class Hotel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10, unique=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10, unique=True)


class RoomManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10, unique=True)
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


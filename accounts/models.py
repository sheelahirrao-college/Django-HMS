from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Hotel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=100)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, name, contact, email, role, hotel, username, password=None):
        user = self.model(
            name=name,
            contact=contact,
            email=self.normalize_email(email),
            role=role,
            hotel=hotel,
            username=username,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name, contact, email, role, hotel, username, password=None):
        user = self.create_user(
            name=name,
            contact=contact,
            email=self.normalize_email(email),
            role=role,
            hotel=Hotel.objects.get(id=hotel),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    roles = (
        (0, None),
        (1, 'Room Manager'),
        (2, 'Booking Manager'),
        (3, 'Customer Manager'),
    )

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    role = models.PositiveSmallIntegerField(choices=roles, blank=True, null=True, default=0)
    hotel = models.ForeignKey(Hotel, blank=True, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name', 'contact', 'email', 'role', 'hotel']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=Hotel)
def pre_save_receiver_hotel(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    else:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_receiver_hotel, sender=Hotel)


@receiver(pre_save, sender=Customer)
def pre_save_receiver_customer(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    else:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_receiver_customer, sender=Customer)

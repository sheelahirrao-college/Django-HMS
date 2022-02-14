from django.db import models
from accounts.models import Hotel

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver


class Category(models.Model):
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)
    number = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey(Category, to_field='name', blank=True, on_delete=models.CASCADE)
    booked_from = models.DateField(blank=True, null=True)
    booked_to = models.DateField(blank=True, null=True)
    available = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.number


class RoomService(models.Model):
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    cleaning_required = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    def str(self):
        return self.room


@receiver(pre_save, sender=Category)
def pre_save_receiver_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(str(instance.hotel.id) + "-" + instance.name)
    else:
        instance.slug = slugify(str(instance.hotel.id) + "-" + instance.name)


pre_save.connect(pre_save_receiver_category, sender=Category)


@receiver(pre_save, sender=Room)
def pre_save_receiver_room(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(str(instance.hotel.id) + "-" + instance.number)
    else:
        instance.slug = slugify(str(instance.hotel.id) + "-" + instance.number)


pre_save.connect(pre_save_receiver_room, sender=Room)


@receiver(pre_save, sender=RoomService)
def pre_save_receiver_room_service(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.room)
    else:
        instance.slug = slugify(instance.room)


pre_save.connect(pre_save_receiver_room_service, sender=RoomService)

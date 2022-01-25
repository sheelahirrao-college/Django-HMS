from django.db import models
from hotel.models import Hotel

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver


class Room(models.Model):
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=100)
    image = models.ImageField(upload_to="room-images")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.number


class Category(models.Model):
    name = models.CharField(max_length=100)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Room)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(str(instance.hotel.id) + "-" + instance.number)

pre_save.connect(pre_save_receiver, sender=Room)
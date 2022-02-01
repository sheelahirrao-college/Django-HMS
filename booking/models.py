from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save

from django.db import models

from hotel.models import Hotel
from room.models import Room


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, to_field='number', on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    slug = models.SlugField()


@receiver(pre_save, sender=Booking)
def pre_save_receiver_booking(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.id)
    else:
        instance.slug = slugify(instance.id)


pre_save.connect(pre_save_receiver_booking, sender=Booking)

from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db import models

from accounts.models import Hotel, Customer
from room.models import Room


class Booking(models.Model):
    customer = models.ForeignKey(Customer, blank=True, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, to_field='number', on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.slug


@receiver(pre_save, sender=Booking)
def pre_save_receiver_booking(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(str(instance.customer) + '-' + str(instance.hotel) + '-' + str(instance.room))
    else:
        instance.slug = slugify(str(instance.customer) + '-' + str(instance.hotel) + '-' + str(instance.room))


pre_save.connect(pre_save_receiver_booking, sender=Booking)

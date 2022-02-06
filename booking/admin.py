from django.contrib import admin
from .models import Booking
from accounts.models import Hotel
from room.models import Room


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'hotel', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')
    search_fields = ('id', 'room', 'hotel', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.is_hotel is True:
            try:
                hotel = Hotel.objects.get(user=request.user)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return 'Hotel Does Not Exist'
        else:
            return 'You are not Hotel'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)
        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return 'Hotel Does Not Exist'

        form.base_fields['room'].queryset = Room.objects.filter(hotel=hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(user=request.user)
        form.base_fields['hotel'].initial = hotel

        return form


admin.site.register(Booking, BookingAdmin)

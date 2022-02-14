from django.contrib import admin, messages
from .models import Booking
from accounts.models import Hotel, Customer
from room.models import Room


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'hotel', 'room', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')
    search_fields = ('id', 'customer', 'hotel', 'room', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.role == 2:
            try:
                hotel = Hotel.objects.get(id=request.user.hotel.id)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return messages.error(request, 'Hotel Does Not Exist')
        else:
            return messages.error(request, 'You Are Not A Booking Manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            hotel = request.user.hotel.id
            return qs.filter(hotel=hotel)

    def get_form(self, request, obj, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)

        try:
            hotel = Hotel.objects.get(id=request.user.hotel.id)
        except Hotel.DoesNotExist:
            return messages.error(request, 'Hotel Does Not Exist')

        form.base_fields['customer'].queryset = Customer.objects.filter(hotel=request.user.hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.hotel.id)
        form.base_fields['hotel'].initial = hotel
        form.base_fields['room'].queryset = Room.objects.filter(hotel=hotel)

        return form


admin.site.register(Booking, BookingAdmin)

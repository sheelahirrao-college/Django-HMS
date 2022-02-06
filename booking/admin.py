from django.contrib import admin
from .models import Booking
from accounts.models import Hotel, Customer
from room.models import Room


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'room', 'hotel', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')
    search_fields = ('id', 'customer', 'room', 'hotel', 'booked_on', 'start_date', 'end_date', 'no_of_days', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.is_customer is True:
            try:
                hotel = Hotel.objects.get(user=request.user)
                obj.hotel = hotel
                obj.customer = request.user
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

        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return 'Customer Does Not Exist'

        form.base_fields['room'].queryset = Room.objects.filter(hotel=hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(user=request.user)
        form.base_fields['hotel'].initial = hotel
        form.base_fields['customer'].queryset = Customer.objects.filter(user=request.user)
        form.base_fields['customer'].initial = customer

        return form


admin.site.register(Booking, BookingAdmin)

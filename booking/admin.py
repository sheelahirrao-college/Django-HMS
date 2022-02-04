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
        obj.hotel = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['room'].queryset = Room.objects.filter(hotel=request.user.id)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.id)
        form.base_fields['hotel'].initial = request.user

        return form


admin.site.register(Booking, BookingAdmin)

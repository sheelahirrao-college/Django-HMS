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
        if request.user.is_customer is True:
            try:
                customer = Customer.objects.get(user=request.user)
                obj.customer = customer
                obj.save()
            except Customer.DoesNotExist:
                return messages.error(request, 'Customer Does Not Exist')
        else:
            return messages.error(request, 'You are not Customer User')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            user = request.user
            if user.is_customer is True:
                try:
                    customer = Customer.objects.get(user=user)
                    return qs.filter(customer=customer)
                except Customer.DoesNotExist:
                    return messages.error(request, 'Customer Does Not Exist')

    def get_form(self, request, obj, **kwargs):
        form = super(BookingAdmin, self).get_form(request, obj, **kwargs)

        if request.user.is_customer is True:
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                return messages.error(request, 'Customer Does Not Exist')
        else:
            return messages.error(request, 'You are not Customer User')

        form.base_fields['customer'].initial = customer

        return form


admin.site.register(Booking, BookingAdmin)

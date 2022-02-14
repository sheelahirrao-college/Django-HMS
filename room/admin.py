from django.contrib import admin, messages

from .models import Room, Category, RoomService
from accounts.models import Hotel


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'slug')
    search_fields = ('id', 'name', 'hotel', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.role == 1:
            try:
                hotel = Hotel.objects.get(id=request.user.hotel.id)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return messages.error(request, 'Hotel Does Not Exist')
        else:
            return messages.error(request, 'You Are Not A Room Manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            hotel = request.user.hotel.id
            return qs.filter(hotel=hotel)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)

        try:
            hotel = Hotel.objects.get(id=request.user.hotel.id)
        except Hotel.DoesNotExist:
            return messages.error(request, 'Hotel Does Not Exist')

        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.hotel.id)
        form.base_fields['hotel'].initial = hotel

        return form


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'hotel', 'booked_from', 'booked_to', 'available', 'slug')
    search_fields = ('id', 'number', 'category', 'hotel', 'booked_from', 'booked_to', 'available', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.role == 1:
            try:
                hotel = Hotel.objects.get(id=request.user.hotel.id)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return messages.error(request, 'Hotel Does Not Exist')
        else:
            return messages.error(request, 'You Are Not A Room Manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            hotel = request.user.hotel.id
            return qs.filter(hotel=hotel)

    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)

        try:
            hotel = Hotel.objects.get(id=request.user.hotel.id)
        except Hotel.DoesNotExist:
            return messages.error(request, 'Hotel Does Not Exist')

        form.base_fields['category'].queryset = Category.objects.filter(hotel=hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.hotel.id)
        form.base_fields['hotel'].initial = hotel
        return form


class RoomServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'room', 'cleaning_required', 'slug')
    search_fields = ('id', 'hotel', 'room', 'cleaning_required', 'slug')

    filter_horizontal = ()
    list_filter = ()

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.role == 1:
            try:
                hotel = Hotel.objects.get(id=request.user.hotel.id)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return messages.error(request, 'Hotel Does Not Exist')
        else:
            return messages.error(request, 'You Are Not A Room Manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            hotel = request.user.hotel.id
            return qs.filter(hotel=hotel)

    def get_form(self, request, obj=None, **kwargs):
        form = super(RoomServiceAdmin, self).get_form(request, obj, **kwargs)

        try:
            hotel = Hotel.objects.get(id=request.user.hotel.id)
        except Hotel.DoesNotExist:
            return messages.error(request, 'Hotel Does Not Exist')

        form.base_fields['room'].queryset = Room.objects.filter(hotel=hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.hotel.id)
        form.base_fields['hotel'].initial = hotel
        return form


admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RoomService, RoomServiceAdmin)

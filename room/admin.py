from django.contrib import admin

from .models import Room, Category
from accounts.models import Hotel


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'image', 'hotel', 'booked_from', 'booked_to', 'available', 'slug')
    search_fields = ('id', 'number', 'category', 'image', 'hotel', 'booked_from', 'booked_to', 'available', 'slug')

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
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return 'Hotel Does Not Exist'
        form.base_fields['category'].queryset = Category.objects.filter(hotel=hotel)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(user=request.user)
        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return 'Hotel Does Not Exist'
        form.base_fields['hotel'].initial = hotel
        return form


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'slug')
    search_fields = ('id', 'name', 'hotel', 'slug')

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
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(user=request.user)
        try:
            hotel = Hotel.objects.get(user=request.user)
        except Hotel.DoesNotExist:
            return 'Hotel Does Not Exist'
        form.base_fields['hotel'].initial = hotel
        return form


admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)

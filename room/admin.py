from django.contrib import admin

from .models import Room, Category
from hotel.models import Hotel


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'category', 'image', 'hotel', 'available', 'slug')
    search_fields = ('id', 'number', 'category', 'image', 'hotel', 'available', 'slug')

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
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = Category.objects.filter(hotel=request.user.id)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.id)
        form.base_fields['hotel'].initial = request.user

        return form


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'slug')
    search_fields = ('id', 'name', 'hotel', 'slug')

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
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.id)
        form.base_fields['hotel'].initial = request.user.id
        return form


admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)

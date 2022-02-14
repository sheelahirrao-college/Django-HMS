from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Hotel, Customer


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'name', 'contact', 'email', 'role', 'hotel', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin', 'is_superuser')
    search_fields = ('id', 'name', 'contact', 'email', 'role', 'hotel', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin', 'is_superuser')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'contact', 'email', 'role', 'hotel', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'contact', 'email', 'role', 'hotel', 'username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    ordering = ('id',)


class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'slug')
    search_fields = ('id', 'name', 'contact', 'slug')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'contact', 'slug')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'contact', 'slug')
        }),
    )

    ordering = ('id',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'hotel', 'slug')
    search_fields = ('id', 'name', 'contact', 'hotel', 'slug')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'contact', 'hotel', 'slug')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'contact', 'hotel', 'slug')
        }),
    )

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if request.user.role == 3:
            try:
                hotel = Hotel.objects.get(id=request.user.hotel.id)
                obj.hotel = hotel
                obj.save()
            except Hotel.DoesNotExist:
                return messages.error(request, 'Hotel Does Not Exist')
        else:
            return messages.error(request, 'You Are Not A Customer Manager')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            hotel = request.user.hotel.id
            return qs.filter(hotel=hotel)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomerAdmin, self).get_form(request, obj, **kwargs)

        try:
            hotel = Hotel.objects.get(id=request.user.hotel.id)
        except Hotel.DoesNotExist:
            return messages.error(request, 'Hotel Does Not Exist')

        form.base_fields['hotel'].queryset = Hotel.objects.filter(id=request.user.hotel.id)
        form.base_fields['hotel'].initial = hotel

        return form


admin.site.register(User, UserAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Customer, CustomerAdmin)

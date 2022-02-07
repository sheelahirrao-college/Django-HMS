from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User, Hotel, RoomManager, Customer


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'usertype', 'date_joined', 'last_login', 'is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email', 'usertype', 'date_joined', 'last_login', 'is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'usertype', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'usertype', 'username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active', 'groups', 'user_permissions')
        }),
    )

    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        if obj.usertype == 1:
            obj.is_hotel = True
            obj.is_room_manager = False
            obj.is_customer = False
        elif obj.usertype == 2:
            obj.is_room_manager = True
            obj.is_hotel = False
            obj.is_customer = False
        elif obj.usertype == 3:
            obj.is_customer = True
            obj.is_hotel = False
            obj.is_customer = False
        else:
            return messages.error(request, 'Usertype is required')
        obj.save()


class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'user')
    search_fields = ('id', 'name', 'contact', 'user')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'contact')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'name', 'contact')
        }),
    )

    ordering = ('id',)


class RoomManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'hotel', 'user')
    search_fields = ('id', 'name', 'contact', 'hotel', 'user')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'contact', 'hotel')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'name', 'contact', 'hotel')
        }),
    )

    ordering = ('id',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact', 'user')
    search_fields = ('id', 'name', 'contact', 'user')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'contact')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'name', 'contact')
        }),
    )

    ordering = ('id',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(RoomManager, RoomManagerAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(User, UserAdmin)

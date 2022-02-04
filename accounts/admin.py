from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Hotel, RoomManager, Customer


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'date_joined', 'last_login', 'is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email', 'date_joined', 'last_login', 'is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_hotel', 'is_room_manager', 'is_customer', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    ordering = ('id',)


class HotelAdmin(BaseUserAdmin):
    list_display = ('id', 'name', 'contact')
    search_fields = ('id', 'name', 'contact')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'contact', 'username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    ordering = ('id',)


class RoomManagerAdmin(BaseUserAdmin):
    list_display = ('id', 'name', 'contact', 'hotel')
    search_fields = ('id', 'name', 'contact', 'hotel')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact', 'username', 'password', 'hotel')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'contact', 'username', 'password1', 'password2', 'hotel')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    ordering = ('id',)


class CustomerAdmin(BaseUserAdmin):
    list_display = ('id', 'name', 'contact')
    search_fields = ('id', 'name', 'contact')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'contact', 'username', 'password')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'contact', 'username', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')
        }),
    )

    ordering = ('id',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(RoomManager, RoomManagerAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Hotel

class HotelAdmin(BaseUserAdmin):
    list_display = ('name', 'description', 'email', 'contact', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('name', 'description', 'email', 'contact', 'is_superuser', 'is_admin', 'is_staff', 'is_active')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'email', 'contact', 'username', 'password')
        }),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('name', 'description', 'email', 'contact', 'username', 'password')
        }),
    )

    ordering = ('name',)

admin.site.register(Hotel, HotelAdmin)
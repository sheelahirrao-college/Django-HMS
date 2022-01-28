from django.contrib import admin

from .models import Room, Category


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


admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)

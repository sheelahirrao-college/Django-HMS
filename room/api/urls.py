from django.urls import path
from .views import (
    room_detail_api_view,
    room_create_api_view,
    room_delete_api_view,
    room_update_api_view,
    all_rooms_api_view,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'room'

urlpatterns = [
    path('allroomsapi', all_rooms_api_view, name='all-rooms-api'),
    path('roomdetailapi/<slug>', room_detail_api_view, name='room-detail-api'),
    path('roomupdateapi/<slug>', room_update_api_view, name='room-update-api'),
    path('roomdeleteapi/<slug>', room_delete_api_view, name='room-delete-api'),
    path('roomcreateapi', room_create_api_view, name='room-create-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

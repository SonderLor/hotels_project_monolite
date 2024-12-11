from django.contrib import admin
from .models import RoomType, Room, Image


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'type', 'price_per_night', 'is_available', 'total_bookings')
    list_filter = ('type', 'is_available', 'hotel')
    search_fields = ('name', 'hotel__name', 'type__name')
    fieldsets = (
        (None, {'fields': ('name', 'hotel', 'type', 'price_per_night', 'is_available')}),
        ('Stats', {'fields': ('total_bookings',)}),
        ('Images', {'fields': ('preview_image',)}),
    )


@admin.register(Image)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'uploaded_at')
    search_fields = ('room__name',)
    ordering = ('-uploaded_at',)

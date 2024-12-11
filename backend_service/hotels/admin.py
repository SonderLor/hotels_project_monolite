from django.contrib import admin
from .models import HotelType, Hotel, Image


@admin.register(HotelType)
class HotelTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'country', 'rating', 'type')
    list_filter = ('type', 'rating', 'city', 'country')
    search_fields = ('name', 'owner__email', 'city', 'country')
    fieldsets = (
        (None, {'fields': ('name', 'address', 'city', 'country', 'description', 'type', 'rating')}),
        ('Images', {'fields': ('preview_image',)}),
        ('Owner Info', {'fields': ('owner',)}),
    )


@admin.register(Image)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'uploaded_at')
    search_fields = ('hotel__name',)
    ordering = ('-uploaded_at',)

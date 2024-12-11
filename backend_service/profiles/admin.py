from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'bio', 'location', 'birth_date', 'total_bookings')
    search_fields = ('user__email', 'username', 'location')
    fieldsets = (
        (None, {'fields': ('user', 'username', 'bio', 'location', 'birth_date')}),
        ('Stats', {'fields': ('total_bookings',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
    )

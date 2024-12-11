from django.db import models
from django.conf import settings


def profile_picture_upload_path(instance, filename):
    return f"pictures/profiles/{instance.user.email}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User"
    )
    username = models.CharField(max_length=100, verbose_name="Username")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Location")
    total_bookings = models.BigIntegerField(default=0, verbose_name="Total Bookings")
    profile_picture = models.ImageField(
        upload_to=profile_picture_upload_path,
        blank=True,
        null=True,
        verbose_name="Profile Picture"
    )

    def __str__(self):
        return f"Profile of {self.user.email}"

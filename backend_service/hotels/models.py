from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def preview_image_upload_path(instance, filename):
    return f"pictures/hotels/{instance.name}/preview/{filename}"


def images_upload_path(instance, filename):
    return f"pictures/hotels/{instance.hotel.name}/images/{filename}"


class HotelType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotels",
        verbose_name="Owner"
    )
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    type = models.ForeignKey(HotelType, on_delete=models.SET_NULL, null=True, related_name='hotels')
    preview_image = models.ImageField(upload_to=preview_image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=images_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Hotel: {self.hotel}"

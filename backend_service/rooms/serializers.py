from rest_framework import serializers
from .models import Room, RoomType, Image
from hotels.models import Hotel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'uploaded_at', 'room')
        read_only_fields = ('id', 'uploaded_at')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('name', 'description')


class RoomSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        queryset=RoomType.objects.all(),
        slug_field='name'
    )
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    hotel_name = serializers.SerializerMethodField()
    hotel_type = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'price_per_night', 'is_available', 'type', 'hotel', 'hotel_name', 'hotel_type', 'address', 'city', 'country', 'images', 'preview_image', 'total_bookings')
        read_only_fields = ('id', 'images', 'total_bookings')

    def get_hotel_name(self, obj):
        return obj.hotel.name

    def get_hotel_type(self, obj):
        return obj.hotel.type.name

    def get_address(self, obj):
        return obj.hotel.address

    def get_city(self, obj):
        return obj.hotel.city

    def get_country(self, obj):
        return obj.hotel.country

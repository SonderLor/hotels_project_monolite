from rest_framework import serializers
from .models import Booking
from rooms.models import Room
from rooms.serializers import RoomSerializer
from auth_app.serializers import CustomUserSerializer
from auth_app.models import CustomUser


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user_id', 'room_id', 'start_date', 'end_date', 'created_at', 'updated_at', 'status']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        room = data.get('room')

        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "End date must be after start date."
                )

            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date,
                status__in=["active", "confirmed"]
            )
            if overlapping_bookings.exists():
                raise serializers.ValidationError(
                    "This room is already booked for the selected dates."
                )

        return data
    
    def create(self, validated_data):
        user = validated_data.pop('user_id')
        room = validated_data.pop('room_id')
        booking = Booking.objects.create(user=user, room=room, **validated_data)
        return booking


class MyBookingsSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'room', 'user', 'start_date', 'end_date', 'created_at', 'updated_at', 'status']
        read_only_fields = ['id', 'room', 'user', 'created_at', 'updated_at']

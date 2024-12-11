from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user_id",
            "username",
            "bio",
            "birth_date",
            "location",
            "total_bookings",
            "profile_picture",
        ]
        read_only_fields = ["id", "user_id", "total_bookings"]

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from profiles.models import Profile
from rooms.models import Room
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Booking)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Signal triggered for Booking id={instance.id}, user={instance.user}")
        try:
            profile = Profile.objects.get(user=instance.user)
            profile.total_bookings += 1
            profile.save()
            logger.info(f"Profile updated: user={instance.user}, total_bookings={profile.total_bookings}")
        except Profile.DoesNotExist:
            logger.error(f"Profile not found for user={instance.user}")

        try:
            room = Room.objects.get(id=instance.room.id)
            room.total_bookings += 1
            room.save()
            logger.info(f"Room updated: room_id={instance.room.id}, total_bookings={room.total_bookings}")
        except Room.DoesNotExist:
            logger.error(f"Room not found: room_id={instance.room.id}")

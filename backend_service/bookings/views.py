from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer, MyBookingsSerializer
import logging

logger = logging.getLogger(__name__)


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.select_related('room', 'user')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info("Fetching bookings list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving booking ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Booking retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new booking with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Booking created successfully: %s", response.data)
        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating booking ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Booking updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting booking ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Booking deleted successfully for ID: %s", kwargs['pk'])
        return response
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        logger.info("Fetching current user's bookings for user ID: %s", request.user.id)
        bookings = Booking.objects.filter(user=request.user).select_related('room', 'user')
        serializer = MyBookingsSerializer(bookings, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def owner(self, request):
        logger.info("Fetching current user's hotel's bookings for user ID: %s", request.user.id)
        bookings = Booking.objects.filter(room__hotel__owner=request.user).select_related('room', 'user')
        serializer = MyBookingsSerializer(bookings, many=True, context={"request": request})
        return Response(serializer.data)

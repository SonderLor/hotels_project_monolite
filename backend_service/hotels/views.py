from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import DatabaseError
from django.core.exceptions import ValidationError
from .models import Hotel, HotelType, Image
from .serializers import HotelSerializer, HotelTypeSerializer, ImageSerializer
from rooms.serializers import RoomSerializer
from .filters import search_accommodations
import logging

logger = logging.getLogger(__name__)


def search_view(request):
    """
    Handles search for hotels and rooms with optional filters.
    """
    logger.debug("Search request received.")
    try:
        params = request.GET.dict()
        logger.debug(f"Received search parameters: {params}")

        show_rooms_only = params.pop("show_rooms_only", "false").lower() == "true"
        logger.debug(f"Show rooms only: {show_rooms_only}")

        hotels, rooms = search_accommodations(params)

        context = {
            "request": request,
            "params": params,
        }

        if show_rooms_only:
            room_serializer = RoomSerializer(rooms, many=True, context=context)
            logger.info("Returning serialized rooms.")
            return JsonResponse({"rooms": room_serializer.data}, status=status.HTTP_200_OK)

        hotel_serializer = HotelSerializer(hotels, many=True, context=context)
        room_serializer = RoomSerializer(rooms, many=True, context=context)

        logger.info("Returning serialized hotels and rooms.")
        return JsonResponse({
            "hotels": hotel_serializer.data,
            "rooms": room_serializer.data
        }, status=status.HTTP_200_OK)

    except ValidationError as ve:
        logger.error(f"Validation error in serializers: {ve}")
        return JsonResponse({"error": "Invalid input parameters", "details": ve.detail}, status=status.HTTP_400_BAD_REQUEST)

    except DatabaseError as db_err:
        logger.critical(f"Database error occurred: {db_err}")
        return JsonResponse({"error": "Internal server error. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        return JsonResponse({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HotelTypeViewSet(ModelViewSet):
    queryset = HotelType.objects.all()
    serializer_class = HotelTypeSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching all hotel types")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving hotel type ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Hotel type retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new hotel type with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Hotel type created successfully: %s", response.data)
        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating hotel type ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Hotel type updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting hotel type ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Hotel type deleted successfully for ID: %s", kwargs['pk'])
        return response


class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.prefetch_related('rooms').prefetch_related('images')
    serializer_class = HotelSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching hotels list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving hotel ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Hotel retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new hotel with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Hotel created successfully: %s", response.data)
        return response

    def perform_create(self, serializer):
        logger.info("Setting owner for the new hotel as user ID: %s", self.request.user.id)
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        logger.info("Updating hotel ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Hotel updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting hotel ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Hotel deleted successfully for ID: %s", kwargs['pk'])
        return response
    
    @action(detail=False, methods=['get'], permission_classes=[])
    def me(self, request):
        logger.info("Fetching current user's hotels for user ID: %s", request.user.id)
        hotels = Hotel.objects.filter(owner=request.user)
        serializer = self.get_serializer(hotels, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[])
    def bookings(self, request):
        logger.info("Fetching current user's hotel's bookings for user ID: %s", request.user.id)
        hotels = Hotel.objects.filter(owner=request.user).prefetch_related(
            'rooms__bookings', 'rooms__type'
        )
        serializer = self.get_serializer(hotels, many=True)
        return Response(serializer.data)


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching images list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving image ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Image retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new image with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Image created successfully: %s", response.data)
        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating image ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Image updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting image ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Image deleted successfully for ID: %s", kwargs['pk'])
        return response

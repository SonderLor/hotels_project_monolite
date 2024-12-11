from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Room, RoomType, Image
from .serializers import RoomSerializer, RoomTypeSerializer, ImageSerializer
import logging

logger = logging.getLogger(__name__)


class RoomTypeViewSet(ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching all room types")
        return super().list(request, *args, **kwargs)


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.select_related('hotel')
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Fetching rooms list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving room ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Room retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new room with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Room created successfully: %s", response.data)
        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating room ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Room updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting room ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Room deleted successfully for ID: %s", kwargs['pk'])
        return response


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

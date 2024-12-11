from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Profile
from .serializers import ProfileSerializer
import logging

logger = logging.getLogger(__name__)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching profiles list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving profile ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Profile retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new profile with data: %s", request.data)
        response = super().create(request, *args, **kwargs)
        logger.info("Profile created successfully: %s", response.data)
        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating profile ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("Profile updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting profile ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("Profile deleted successfully for ID: %s", kwargs['pk'])
        return response

    @action(detail=False, methods=['get'], permission_classes=[])
    def me(self, request):
        logger.info("Fetching current user profile for user ID: %s", request.user.id)
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

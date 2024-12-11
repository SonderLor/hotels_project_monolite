from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet, ImageViewSet

router = DefaultRouter()
router.register('types', RoomTypeViewSet, basename='hotel-type')
router.register('rooms', RoomViewSet, basename='hotel')
router.register('images', ImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
]

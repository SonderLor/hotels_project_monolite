from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, HotelTypeViewSet, ImageViewSet, search_view

router = DefaultRouter()
router.register('types', HotelTypeViewSet, basename='hotel-type')
router.register('hotels', HotelViewSet, basename='hotel')
router.register('images', ImageViewSet, basename='image')

urlpatterns = [
    path('search/', search_view, name='search'),
    path('', include(router.urls)),
]

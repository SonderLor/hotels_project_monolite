from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, csrf, LoginView, LogoutView

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('csrf/', csrf, name='csrf'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]

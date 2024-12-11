from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import Group
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
import logging

logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


class LoginView(APIView):
    """
    Custom endpoint for user login.
    """
    def post(self, request):
        logger.debug("User login process started.")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            logger.debug(f"Authentication attempt for email: {email}")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {email} logged in successfully.")
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"Failed login attempt for email: {email}")
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.error("Validation error during login.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Custom endpoint for user logout.
    """
    def post(self, request):
        logger.debug("User logout process started.")
        if request.user.is_authenticated:
            email = request.user.email
            logout(request)
            logger.info(f"User {email} logged out successfully.")
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            logger.warning("Logout attempt by an unauthenticated user.")
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        logger.info("Fetching users list")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("Retrieving user ID: %s", kwargs['pk'])
        response = super().retrieve(request, *args, **kwargs)
        logger.info("User retrieved successfully for ID: %s", kwargs['pk'])
        return response

    def create(self, request, *args, **kwargs):
        logger.info("Attempting to create a new user with data: %s", request.data)

        if 'email' not in request.data:
            logger.error("Email is missing in request data.")
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if 'password' not in request.data:
            logger.error("Password is missing in request data.")
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if CustomUser.objects.filter(email=request.data.get('email')).exists():
            return JsonResponse({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        group_name = request.data.get('group_name')
        if not group_name:
            logger.error("Group name is missing in request data.")
            return Response(
                {"error": "Group name is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            logger.error("Group '%s' does not exist.", group_name)
            return Response(
                {"error": f"Group '{group_name}' does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = serializer.save()
            user.groups.add(group) 
            logger.info("User created successfully and added to group '%s'.", group_name)
        except Exception as e:
            logger.exception("Error occurred while creating user: %s", str(e))
            return Response(
                {"error": "An error occurred while creating the user."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info("Updating user ID: %s with data: %s", kwargs['pk'], request.data)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info("User updated successfully for ID: %s", kwargs['pk'])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info("Deleting user ID: %s", kwargs['pk'])
        response = super().destroy(request, *args, **kwargs)
        logger.info("User deleted successfully for ID: %s", kwargs['pk'])
        return response

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        logger.info("Fetching current user info for user ID: %s", request.user.id)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

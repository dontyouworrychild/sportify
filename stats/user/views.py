from rest_framework import filters, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .enums import TokenEnum
from .models import Token, User
from .serializers import (AuthTokenSerializer,
                          CreatePasswordFromResetOTPSerializer,
                          CustomObtainTokenPairSerializer, UsernameSerializer,
                          ListUserSerializer, PasswordChangeSerializer,
                          InitiatePasswordResetSerializer,
                          UpdateUserSerializer)
from .permissions import IsOwner, IsAdmin

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Authentication'])
class CustomObtainTokenPairView(TokenObtainPairView):
    """Authenticate with username and password"""
    serializer_class = CustomObtainTokenPairSerializer

@extend_schema(tags=['Password'])
class AuthViewsets(viewsets.GenericViewSet):
    """Auth viewsets"""
    serializer_class = UsernameSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["initiate_reset_password", "reset_password"]:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=InitiatePasswordResetSerializer,
        url_path="initiate-reset-password",
    )
    def initiate_reset_password(self, request, pk=None):
        """Send temporary OTP to the user phone number to be used for password reset"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True,
                         "message": "Temporary OTP sent to your mobile!"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, serializer_class=CreatePasswordFromResetOTPSerializer, url_path='reset-password')
    def reset_password(self, request, pk=None):
        """Create a new password by using the OTP that was sent to the phone number"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token: Token = Token.objects.filter(
            token=request.data['otp'], phone_number=request.data['phone_number'],  token_type=TokenEnum.PASSWORD_RESET).first()
        if not token or not token.is_valid():
            return Response({'success': False, 'errors': 'Invalid password reset otp or phone number'}, status=400)
        token.reset_user_password(request.data['new_password'])
        token.delete()
        return Response({'success': True, 'message': 'Password successfully reset'}, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=False, serializer_class=PasswordChangeSerializer, url_path='change-password')
    def change_password(self, request):
        '''Allows password change to authenticated user.'''
        context = {"request": request}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Your password has been updated."}, status=status.HTTP_200_OK)
    

# class PasswordChangeView(viewsets.GenericViewSet):
#     '''Allows password change to authenticated user.'''
#     serializer_class = PasswordChangeSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request):
#         context = {"request": request}
#         serializer = self.get_serializer(data=request.data, context=context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Your password has been updated."}, status=status.HTTP_200_OK)

@extend_schema(tags=['Authentication'])
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "created": created, "roles": user.roles},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=['User'])
class UserViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "list", "patch"]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["first_name", "last_name"]
    ordering_fields = [
        "created_at",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    ]

    def get_queryset(self):
        return super().get_queryset().filter(is_admin=False)

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ["list", "get"]:
            permission_classes = [AllowAny]
        elif self.action in ["partial_update"]:
            permission_classes = [IsOwner]
        elif self.action in ["create", "destroy"]:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return UpdateUserSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()

        # Check if the request contains an updated image
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Get the updated image from the serializer's data
        updated_image = serializer.validated_data.get('image')

        # If there is an updated image, delete the existing image if it exists
        if updated_image:
            user.delete_image()

        # Save the new image to the user's profile
        user.image = updated_image
        user.save(update_fields=["image"])

        return Response({"message": "Image updated successfully."}, status=status.HTTP_200_OK)
    
    # @action(detail=False, methods=['get'], url_path='(?P<username>\w+)')
    # def retrieve_by_username(self, request, username=None):
    #     try:
    #         user = User.objects.get(username=username)
    #         serializer = ListUserSerializer(user)
    #         return Response(serializer.data)
    #     except User.DoesNotExist:
    #         return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
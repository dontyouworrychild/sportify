from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone

from .models import User, Token

from .utils import validate_phone_number, generate_otp, is_admin_user
from .enums import TokenEnum
from .tasks import send_phone_notification
from django.contrib.auth.hashers import make_password

class CustomObtainTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access_token = refresh.access_token
        self.user.save_last_login()
        data["refresh"] = str(refresh)
        data["access"] = str(access_token)
        return data
    

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username:
            user = authenticate(request=self.context.get(
                "request"), username=username, password=password)

        if not user:
            message = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(message, code="authentication")
        attrs["user"] = user
        return attrs

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, min_length=5)

    def validate_old_password(self, value):
        request = self.context["request"]

        if not request.user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        user: User = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=["password"])


class CreatePasswordFromResetOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)

class InitiatePasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs: dict):
        not_validated_phone_number = attrs.get('phone_number')
        phone_number = validate_phone_number(not_validated_phone_number.strip())
        user = User.objects.filter(phone_number=phone_number, is_active=True).first()
        if not user:
            raise serializers.ValidationError({'phone_number':'Phone number not registered.'})
        attrs['phone_number'] = phone_number
        attrs['user'] =  user
        return super().validate(attrs)
    
    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user = validated_data.get('user')
        otp = generate_otp()
        token,_ = Token.objects.update_or_create(
            user=user,
            token_type=TokenEnum.PASSWORD_RESET,
            defaults={
                "user": user,
                "token_type": TokenEnum.PASSWORD_RESET,
                "token": otp,
                "phone_number": phone_number,
                "created_at": datetime.now(timezone.utc),
            }
        )

        message_info = {
            'message': f"\nUse {otp} to reset your password.\nIt expires in 10 minutes",
            'phone_number': phone_number
        }

        send_phone_notification.delay(message_info)
        return token
    
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "username",
            "image",
            "created_at",
            "role",
        ]

        extra_kwargs = {
            "role": {"read_only": True},
            "created_at": {"read_only": True}
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('image', )
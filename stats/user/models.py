import os
import uuid
from datetime import datetime, timezone


from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


from .managers import CustomUserManager
from .enums import TOKEN_TYPE_CHOICE, ROLE_CHOICE

def default_role():
    return ["admin"]

def image_directory_path(instance, filename):
    role = "other"
    if hasattr(instance, 'role'):
        role = instance.role

    extension = filename.split('.')[-1]
    return f"{role}/{instance.id}.{extension}"

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        validators=[RegexValidator(
                regex='^[a-z0-9_]+$',
                message='Username can only contain lowercase letters, numbers, and underscores.',
                code='invalid_username'
            ),
        ],
    )
    phone_number = models.CharField(
        _("phone_number"), max_length=30, unique=True)
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    first_name = models.CharField(_("first_name"), max_length=150, blank=True)
    last_name = models.CharField(_("last_name"), max_length=150, blank=True)
    # location = models.CharField(_("location"))

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number"]
    objects = CustomUserManager()
    role = models.CharField(max_length=20, choices=ROLE_CHOICE, null=True, blank=True)
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.username}: {self.role}"
    
    def validate_password(self, value: str) -> str:
        return make_password(value)
    
    def delete_image(self):
        if self.image:
            # Get the path to the image file
            image_path = self.image.path

            # Delete the image file from the file system
            if os.path.exists(image_path):
                os.remove(image_path)

            # Set the 'image' field to None and save the model to remove the image reference from the database
            self.image = None
            self.save(update_fields=["image"])

    def save_last_login(self) -> None:
        self.last_login = datetime.now()
        self.save(update_fields=["last_login"])


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    token = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=20)
    token_type = models.CharField(max_length=100, choices=TOKEN_TYPE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self) -> bool:
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 )
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def reset_user_password(self, password: str) -> None:
        self.user.set_password(password)
        self.user.save()
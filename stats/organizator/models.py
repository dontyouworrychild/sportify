import uuid
from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _

def unique_filename_generator(filename):
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4}.{extension}"
    return filename

def organizator_directory_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/students/{user_id}/{filename}
    # unique filename will be generated

    unique_filename = unique_filename_generator(filename)

    return f"organizators/{instance.id}/{unique_filename}"

class Organizator(User):
    image = models.ImageField(upload_to=organizator_directory_path, blank=True)

    class Meta:
        verbose_name = _("organizator")
        verbose_name_plural = _("organizators")

    def __str__(self) -> str:
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        self.role = "organizator"
        super().save(*args, **kwargs)

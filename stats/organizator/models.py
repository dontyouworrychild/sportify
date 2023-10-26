from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _

def organizator_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"organizators/{instance.id}.{extension}"

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

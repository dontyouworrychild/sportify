from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _

def organizator_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"organizators/{instance.id}.{extension}"

class Organizator(User):
    class Meta:
        verbose_name = _("organizator")
        verbose_name_plural = _("organizators")

    def __str__(self) -> str:
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        self.role = "organizator"
        super(Organizator, self).save(*args, **kwargs)
        # update_fields = ['role']
        # super(Organizator, self).save(update_fields=update_fields)
        # super().save(*args, **kwargs)

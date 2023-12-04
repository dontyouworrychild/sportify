from django.db import models
from user.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password

def organizator_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"organizators/{instance.id}.{extension}"

class Organizator(User):
    class Meta:
        verbose_name = _("organizator")
        verbose_name_plural = _("organizators")

    def __str__(self) -> str:
        return f"{self.username}"
    
    def validate_password(self, value: str) -> str:
        return make_password(value)
    # def save(self, *args, **kwargs):
    #     self.role = "organizator"
    #     super(Organizator, self).save(*args, **kwargs)
        # update_fields = ['role']
        # super(Organizator, self).save(update_fields=update_fields)
        # super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        self.role = "organizator"
        self.password = self.validate_password(self.password)
        super().save(*args, **kwargs)
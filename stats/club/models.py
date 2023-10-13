import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models

def logo_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    # image will be uploaded to MEDIA_ROOT/clubs/{club_id}.extension}

    return f"clubs/{instance.id}.{extension}"

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name"), max_length=50)
    logo = models.ImageField(upload_to=logo_directory_path, blank=True)

    # Пока что пусь location осылай бола берсын, но в целом, 
    # бир определнный списоктын ишиндегы биреуын тандау керек
    location = models.CharField(_("location"), max_length=50)

    def __str__(self):
        return f"{self.name} - {self.location}"
    
    class Meta:
        verbose_name = _("club")
        verbose_name_plural = _("clubs")

from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid
from coach.models import Coach
from club.models import Club
from django.utils.translation import gettext_lazy as _
from common.enums import SPORT_TYPES

def student_directory_path(instance, filename):
    # image will be uploaded to MEDIA_ROOT/students/{student_id}.extension
    # unique filename will be generated
    extension = filename.split('.')[-1]

    return f"students/{instance.id}.{extension}"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    image = models.ImageField(upload_to=student_directory_path, blank=True)
    coach = models.ForeignKey(Coach, verbose_name=_('coach'), related_name='students', null=True, on_delete=models.SET_NULL)
    club = models.ForeignKey(Club, verbose_name=_('club'), related_name='students', null=True, on_delete=models.SET_NULL)

    # Пока что пусь location осылай бола берсын, но в целом, 
    # бир определнный списоктын ишиндегы биреуын тандау керек
    location = models.CharField(_("location"), max_length=50)

    '''
        !TODO
        еще какие-то field косу керек тут
    '''

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - ({self.club.name}, {self.club.location})"

    

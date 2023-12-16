from django.utils.translation import gettext_lazy as _
from django.db import models
from user.models import User
from club.models import Club
from django.contrib.auth.hashers import make_password

def coach_directory_path(instance, filename):
    extension = filename.split(".")[-1]
    return f"coaches/{instance.id}.{extension}"

class Coach(User):
    club = models.ForeignKey(Club, verbose_name=_("club"), related_name="coaches", null=True, on_delete=models.SET_NULL)

    # Пока что пусь location осылай бола берсын, но в целом, 
    # бир определнный списоктын ишиндегы биреуын тандау керек
    location = models.CharField(_("location"), max_length=50)
    achievement = models.CharField(_("achievement"), blank=True, null=True, max_length=50)


    class Meta:
        verbose_name = _("coach")
        verbose_name_plural = _("coaches")

    def validate_password(self, value: str) -> str:
        return make_password(value)

    # def __str__(self) -> str:
        # return f"{self.first_name} {self.last_name} - ({self.club.name}, {self.club.location})"

    def save(self, *args, **kwargs):
        self.role = "coach"
        self.password = self.validate_password(self.password)
        super().save(*args, **kwargs)

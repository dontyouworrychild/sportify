import uuid
import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from coach.models import Coach
from club.models import Club

def student_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"students/{instance.id}.{extension}"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    image = models.ImageField(upload_to=student_directory_path, blank=True)
    coach = models.ForeignKey(Coach, verbose_name=_('coach'), related_name='students', null=True, on_delete=models.SET_NULL)
    club = models.ForeignKey(Club, verbose_name=_('club'), related_name='students', null=True, on_delete=models.SET_NULL)
    date_of_birth = models.DateField()
    achievement = models.CharField(blank=True, null=True)
    last_republic_result = models.CharField(blank=True, null=True)

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
        if self.club:
            return f"{self.first_name} {self.last_name} - ({self.club.name}, {self.club.location})"
        return f"{self.first_name} {self.last_name}"

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year

class LastRepublicWinner(models.Model):
    year = models.IntegerField(_('year'), choices=year_choices(), default=current_year)
    student = models.ForeignKey(Student, related_name='republic_winners', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.student.first_name} {self.student.last_name} - {self.year}"

    

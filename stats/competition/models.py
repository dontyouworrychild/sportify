import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from organizator.models import Organizator
from student.models import Student
from common.enums import AGE_CATEGORY_CHOICE, WEIGHT_CATEGORY_CHOICE

class Federation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"

class Competition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    # register_students_deadline = models.DateField()
    
    # Дурыстап озгерту керек
    location = models.CharField(_("location"), max_length=50)

    # Хз, тоже дурыстап карау керек
    address = models.CharField(_("address"), max_length=50)
    
    # ArrayField siakty ma etu kerek, так как каждый competitionде бирнеше organizators бола алады
    organizator = models.ForeignKey(Organizator, null=True, blank=True, on_delete=models.SET_NULL)

    federation = models.ForeignKey(Federation, null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name = _("competition")
        verbose_name_plural = _("competitions")

    def __str__(self) -> str:
        return f"{self.name}"

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, related_name='participants', on_delete=models.CASCADE)
    student_info = models.ForeignKey(Student, related_name='competitions', on_delete=models.CASCADE)
    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICE)
    weight_category = models.CharField(max_length=5, choices=WEIGHT_CATEGORY_CHOICE)
    place = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.student_info.first_name} {self.student_info.last_name} - ({self.student_info.club.name}, {self.student_info.club.location} - ({self.place})) : {self.id}"


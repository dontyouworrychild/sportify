from django.db import models
from competition.models import Competition, Participant
from common.enums import AGE_CATEGORY_CHOICE, WEIGHT_CATEGORY_CHOICE
import uuid

WIN_TYPE_CHOICES = (
    ('knockout', 'Техн. нокаут'),
    ('points', 'По очкам'),
)

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, related_name='games', on_delete=models.CASCADE)
    red_corner = models.ForeignKey(Participant, null=True, blank=True, related_name='red_corner_fights', on_delete=models.SET_NULL)
    blue_corner = models.ForeignKey(Participant, null=True, blank=True, related_name='blue_corner_fights', on_delete=models.SET_NULL)
    red_corner_winner = models.BooleanField(default=False)
    blue_corner_winner = models.BooleanField(default=False)
    parent = models.ForeignKey('Game', null=True, on_delete=models.SET_NULL, related_name="parent_fight")
    index = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    win_type = models.CharField(max_length=15, choices=WIN_TYPE_CHOICES, blank=True, null=True)

    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICE)
    weight_category = models.CharField(max_length=5, choices=WEIGHT_CATEGORY_CHOICE)

    def __str__(self) -> str:
        if self.red_corner is not None and self.blue_corner is not None:
            return f"{self.red_corner.student_info.first_name} {self.red_corner.student_info.last_name} - {self.blue_corner.student_info.first_name} {self.blue_corner.student_info.last_name} : {self.level} - {self.competition.name}"
        elif self.red_corner is not None:
            return f"{self.red_corner.student_info.first_name} {self.red_corner.student_info.last_name} - None : {self.level} - {self.competition.name}"
        elif self.blue_corner is not None:
            return f"None - {self.blue_corner.student_info.first_name} {self.blue_corner.student_info.last_name} : {self.level} - {self.competition.name}"
        
        return f"{self.id} : {self.level} - {self.competition.name}"

from django.db import models
from competition.models import Competition, Participant
from common.enums import AGE_CATEGORY_CHOICE, WEIGHT_CATEGORY_CHOICE
import uuid

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(Competition, related_name='games', on_delete=models.CASCADE)
    red_corner = models.ForeignKey(Participant, null=True, blank=True, related_name='red_corner_fights', on_delete=models.SET_NULL)
    blue_corner = models.ForeignKey(Participant, null=True, blank=True, related_name='blue_corner_fights', on_delete=models.SET_NULL)
    parent = models.ForeignKey('Game', null=True, on_delete=models.SET_NULL, related_name="parent_fight")
    index = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    winner = models.ForeignKey(Participant, null=True, blank=True, related_name='won_games', on_delete=models.SET_NULL)
    '''
    WIN_TYPE_CHOICES = (
        ('knockout', 'Knockout'),
        ('point', 'By points'),
        ('no', 'Did not start')
    )
    win_type = models.CharField(max_length=15, choices=WIN_TYPE_CHOICES)
    '''


    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICE)
    weight_category = models.CharField(max_length=5, choices=WEIGHT_CATEGORY_CHOICE)

    def __str__(self) -> str:
        if self.red_corner is not None and self.blue_corner is not None:
            return f"{self.red_corner.participant.first_name} {self.red_corner.participant.last_name} - {self.blue_corner.participant.first_name} {self.blue_corner.participant.last_name} : {self.level}"
        elif self.red_corner is not None:
            return f"{self.red_corner.participant.first_name} {self.red_corner.participant.last_name} - None : {self.level}"
        elif self.blue_corner is not None:
            return f"None - {self.blue_corner.participant.first_name} {self.blue_corner.participant.last_name} : {self.level}"
        
        return f"{self.id} : {self.level}"

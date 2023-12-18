from django.db import models
from competition.models import Competition, Participant
from common.enums import AGE_CATEGORY_CHOICE, WEIGHT_CATEGORY_CHOICE
import uuid

def image_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    return f"news/{instance.id}.{extension}"

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
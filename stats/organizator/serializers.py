from rest_framework import serializers
from .models import Organizator


class OrganizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizator
        fields = [
            "id",
            "first_name",
            "last_name",
            "image",
        ]

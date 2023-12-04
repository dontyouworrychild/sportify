from rest_framework import serializers
from .models import Organizator


class OrganizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizator
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "image",
            "phone_number",
            "password",
            "role",
        ]

class ListOrganizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizator
        fields = [
            "id",
            "first_name",
            "last_name",
            "image"
        ]

class UpdateOrganizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizator
        fields = [
            "image",
        ]
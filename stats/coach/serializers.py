from rest_framework import serializers
from .models import Coach


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "image",
            "club",
            "location",
            "role",
            "phone_number"
        ]

class ListCoachForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = [
            "id",
            "first_name",
            "last_name",
            "image"
        ]

class UpdateCoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = [
            "image"
        ]
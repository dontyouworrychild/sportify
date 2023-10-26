from rest_framework import serializers
from .models import Competition, Participant


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "organizators",
            "location",
            "address",
            "federation"
        ]

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            "id",
            "competition",
            "participant",
            "age_category",
            "weight_category",
            "place"
        ]
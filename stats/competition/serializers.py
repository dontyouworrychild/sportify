from rest_framework import serializers
from .models import Competition, Participant, Game


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
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "competition",
            "red_corner",
            "blue_corner",
            "parent",
            "empty",
            "age_category",
            "weight_category",

        ]

class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "competition",
            "red_corner",
            "blue_corner",
            "fighter1",
            "fighter2",
            "level",
            "empty"
        ]
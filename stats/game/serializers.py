from rest_framework import serializers
from .models import Game
from student.serializers import StudentSerializer
from competition.serializers import ParticipantSerializer

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = [
            "id",
            "red_corner",
            "blue_corner",
            "red_corner_winner",
            "blue_corner_winner",
            "winner",
        ]

class SelectWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'winner',
            'blue_corner_winner',
            'red_corner_winner'
        ]
        
class ListGameSerializer(serializers.ModelSerializer):
    red_corner = ParticipantSerializer(read_only=True)
    blue_corner = ParticipantSerializer(read_only=True)
    class Meta:
        model = Game
        fields = [
            "id",
            "red_corner",
            "blue_corner",
            "red_corner_winner",
            "blue_corner_winner",
        ]
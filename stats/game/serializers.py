from rest_framework import serializers
from .models import Game

class CustomGameListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return data

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "competition",
            "red_corner",
            "blue_corner",
            "parent",
            "age_category",
            "weight_category",
            "winner",
            "level",
            "index"
        ]

        list_serializer_class = CustomGameListSerializer

class UpdateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "winner"
        ]
        
class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "competition",
            "red_corner",
            "blue_corner",
            "winner",
            "level",
            "parent",
        ]
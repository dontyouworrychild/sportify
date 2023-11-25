from rest_framework import serializers
from .models import Game
from competition.serializers import ParticipantSerializer
from competition.models import Participant
from student.models import Student
from club.serializers import ClubSerializer

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = [
            "id",
            "red_corner",
            "blue_corner",
            "red_corner_winner",
            "blue_corner_winner",
        ]

class SelectWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
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

class StudentLastGamesModelStudentSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "club"
        ]

class StudentLastGamesModelParticipantSerializer(serializers.ModelSerializer):
    student_info = StudentLastGamesModelStudentSerializer(read_only=True)
    class Meta:
        model = Participant
        fields = [
            "student_info",
        ]

class StudentLastGamesModelGameSerializer(serializers.ModelSerializer):
    red_corner = StudentLastGamesModelParticipantSerializer(read_only=True)
    blue_corner = StudentLastGamesModelParticipantSerializer(read_only=True)
    result = serializers.SerializerMethodField()
    class Meta:
        model = Game
        fields = [
            "id",
            "red_corner",
            "blue_corner",
            "level",
            "index",
            "result",
            # "red_corner_winner",
            # "blue_corner_winner"
        ]
    
    def get_result(self, obj):
        student_id = self.context.get('student_id', None)
        winner_id = None
        if obj.red_corner_winner and obj.red_corner:
            winner_id = obj.red_corner.student_info.id
        elif obj.blue_corner_winner and obj.blue_corner:
            winner_id = obj.blue_corner.student_info.id
        if winner_id == student_id:
            return "Win"
        return "Lost"
    
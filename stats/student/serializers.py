from rest_framework import serializers
from .models import Student

from club.serializers import ClubSerializer
from coach.serializers import ListCoachForStudentSerializer
# from competition.models import Participant
# from competition.serializers import ListNameCompetitionSerializer
from .models import LastRepublicWinner


class StudentSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    coach = ListCoachForStudentSerializer(read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "image",
            "club",
            "location",
            "coach"
        ]

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "image",
            "club"
        ]

class StudentProfileSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    coach = ListCoachForStudentSerializer(read_only=True)
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "image",
            "club",
            "location",
            "coach",
            "date_of_birth",
            "achievement",
        ]

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "image",
            "club",
            "location",
            "coach",
            "date_of_birth",
            "achievement",
        ]
from rest_framework import serializers
from .models import Student

from club.serializers import ClubSerializer
from coach.serializers import ListCoachForStudentSerializer


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
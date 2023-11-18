from rest_framework import serializers
from coach.serializers import CoachSerializer
from club.serializers import ClubSerializer
from student.serializers import StudentSerializer


class GlobalSearchResultsSerializer(serializers.Serializer):
    students = StudentSerializer(many=True)
    coaches = CoachSerializer(many=True)
    clubs = ClubSerializer(many=True)
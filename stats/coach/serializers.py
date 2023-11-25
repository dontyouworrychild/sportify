from rest_framework import serializers
from .models import Coach
from club.serializers import ClubSerializer
from student.models import Student

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

class StudentBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "image"
        ]

class CoachPageSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)
    students = StudentBasicInfoSerializer(many=True, read_only=True)
    class Meta:
        model = Coach
        fields = [
            "id",
            "first_name",
            "last_name",
            "image",
            "club",
            "students"
        ]

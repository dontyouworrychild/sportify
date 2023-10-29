from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
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
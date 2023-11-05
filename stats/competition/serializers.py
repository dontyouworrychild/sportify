from rest_framework import serializers
from .models import Competition, Participant, Student

CATEGORIES = {
    '6-7': ['24kg', '28kg', '32kg', '36kg', '40kg', '44kg', '48kg'],
    '8-9': ['28kg', '32kg', '36kg', '40kg', '44kg', '48kg', '52kg'],
    '10-11': ['32kg', '36kg', '40kg', '44kg', '48kg', '52kg', '56kg'],
    '12-13': ['36kg', '40kg', '44kg', '48kg', '52kg', '56kg', '60kg'],
    '14-15': ['40kg', '44kg', '48kg', '52kg', '56kg', '60kg', '64kg'],
    '16-17': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg'],
}  

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

class UpdateCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = [
            "start_date",
            "end_date",
            "address"
        ]

class ParticipantSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = [
            "id",
            "competition",
            "participant",
            "age_category",
            "weight_category",
            "place",
            "first_name",
            "last_name",
            "location",
            "club"
        ]

    def get_first_name(self, obj):
        return obj.participant.first_name if obj.participant else None
    
    def get_last_name(self, obj):
        return obj.participant.last_name if obj.participant else None
    
    def get_location(self, obj):
        return obj.participant.location if obj.participant else None

    def get_club(self, obj):
        return obj.participant.club if obj.participant else None


class RegisterStudentSerializer(serializers.Serializer):
    student_id = serializers.UUIDField()
    age_category = serializers.CharField()
    weight_category = serializers.CharField()

    class Meta:
        model = Participant
        fields = [
            "id",
            "competition",
            "age_category",
            "weight_category",
            "student_id",
        ]

    def validate_student_id(self, value):
        competition = self.context.get('competition')
        if competition.participants.filter(participant__id=value).exists():
            raise serializers.ValidationError("Student is already registered for this competition.")
        is_student = Student.objects.filter(id=value).exists()
        if not is_student:
            raise serializers.ValidationError("Student with the provided UUID does not exists.")
        return value

    def validate_age_category(self, value):
        if value not in CATEGORIES:
            raise serializers.ValidationError("Invalid age category for competition.")
        return value

    def validate_weight_category(self, value):
        age_category = self.initial_data.get('age_category')
        if value not in CATEGORIES.get(age_category, []):
            raise serializers.ValidationError("Invalid weight category for competition.")
        return value

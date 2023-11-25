from rest_framework import serializers
from .models import Competition, Participant, Student, Federation, Region

from student.serializers import StudentSerializer
from organizator.serializers import ListOrganizatorSerializer
from drf_spectacular.utils import extend_schema_field

CATEGORIES = {
    '6-7': ['24kg', '28kg', '32kg', '36kg', '40kg', '44kg', '48kg'],
    '8-9': ['28kg', '32kg', '36kg', '40kg', '44kg', '48kg', '52kg'],
    '10-11': ['32kg', '36kg', '40kg', '44kg', '48kg', '52kg', '56kg'],
    '12-13': ['36kg', '40kg', '44kg', '48kg', '52kg', '56kg', '60kg'],
    '14-15': ['40kg', '44kg', '48kg', '52kg', '56kg', '60kg', '64kg'],
    '16-17': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg'],
} 

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "slug",
            "region",
            "image"
        ]

class ListFederationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Federation
        fields = [
            "name"
        ]

class CompetitionSerializer(serializers.ModelSerializer):
    # federation = ListFederationSerializer(read_only=True)
    organizator = ListOrganizatorSerializer(read_only=True)
    federation = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = [
            "id",
            "name",
            "start_date",
            "end_date",
            "organizator",
            "location",
            "address",
            "federation",
            "competition_type",
            "region"
        ]

    @extend_schema_field(serializers.CharField())
    def get_federation(self, obj):
        return obj.federation.name if obj.federation else None

    @extend_schema_field(serializers.CharField())
    def get_region(self, obj):
        # This method returns the string representation of the region
        return obj.region.region if obj.region else None

class UpdateCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = [
            "start_date",
            "end_date",
            "address"
        ]


class ParticipantSerializer(serializers.ModelSerializer):
    student_info = StudentSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = [
            "id",
            "student_info",
            "place",
        ]


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

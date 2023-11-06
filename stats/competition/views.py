from django.db.models import Q
from rest_framework import status, viewsets, exceptions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from game.models import Game
from game.serializers import ListGameSerializer
from organizator.permissions import IsOrganizator
from .models import Competition, Participant
from .serializers import CompetitionSerializer, ParticipantSerializer, UpdateCompetitionSerializer, RegisterStudentSerializer
from .permissions import IsPresident, IsStudentCoach
from .utils import generate_tournament_bracket_logic

CATEGORIES = {
    '6-7': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
    '8-9': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
    '10-11': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
    '12-13': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
    '14-15': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
    '16-17': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg', '72kg', '76kg'],
}  


@extend_schema(tags=['Competition'])
class CompetitionViewsets(viewsets.ModelViewSet):
    queryset = Competition.objects.all().select_related('organizator', 'federation')
    serializer_class = CompetitionSerializer
    # http_method_names = ['get', 'post', 'patch', 'delete']
    http_method_names = ['get', 'patch', 'post']

    def get_permissions(self):
        permission_classes = [AllowAny]
        # if self.action in ['create', 'destroy']:
            # permission_classes = [IsPresident]
        if self.action in ['partial_update']:
            permission_classes = [IsOrganizator, IsPresident]
        elif self.action in ['register_student', 'unregister_student']:
            permission_classes = [IsStudentCoach]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Update Competition Information",
        description="Allows organizers of a competition to partially update information about that competition. "
                    "The information that can be updated includes the competition's start date, end date, and address.",
        request=UpdateCompetitionSerializer,
        responses={
            200: inline_serializer(
                name='UpdateCompetitionResponse',
                fields={
                    'message': serializers.CharField(),
                    'data': UpdateCompetitionSerializer()
                }
            ),
            400: 'Invalid input or missing fields'
    },
    methods=['PATCH']
)
    def partial_update(self, request):
        competition = self.get_object()
        serializer = UpdateCompetitionSerializer(competition, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response({"message": "Competition information updated successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)

    @extend_schema(
        request=RegisterStudentSerializer,
        responses={
            201: inline_serializer(
            name='RegisterStudentResponse',
            fields={
                'message': serializers.CharField(),
                'data': ParticipantSerializer()
            }
        )
        },
        summary='Register a student for the competition',
        description='This endpoint allows coaches to register theirs students for the competition.',
    )
    @action(detail=True, methods=['post'], url_path='register_student')
    def register_student(self, request, pk=None):
        competition = self.get_object() 
        serializer = RegisterStudentSerializer(data=request.data, context={'competition': competition})
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data.get('student_id')
        age_category = serializer.validated_data.get('age_category')
        weight_category = serializer.validated_data.get('weight_category')
        
        participant_data = {
            'participant': student_id,
            'age_category': age_category,
            'weight_category': weight_category,
            'competition': competition.id
        }

        participant_serializer = ParticipantSerializer(data=participant_data)
        participant_serializer.is_valid(raise_exception=True)
        participant_serializer.save()

        return Response({"message": "Student registered successfully.", "data": participant_serializer.data},
                        status=status.HTTP_201_CREATED)
        
    @extend_schema(
        summary='Unregister a student from the competition',
        description='This endpoint allows coaches to unregister their student from the competition.',
    )
    @action(detail=True, methods=['post'], url_path='unregister_student')
    def unregister_student(self, request, pk=None):
        competition = self.get_object()
        student_id = request.data.get('student_id', None)
        if not student_id:
            raise exceptions.NotFound("Please provide student id in the request data.")
        try:
            participant = Participant.objects.get(participant_id=student_id, competition=competition)
        except Participant.DoesNotExist:
            return Response({"error": "Student is not registered for this competition."},
                            status=status.HTTP_400_BAD_REQUEST)
        participant.delete()
        return Response({"message": "Student unregistered successfully."},
                        status=status.HTTP_200_OK)
    
    @extend_schema(
        responses={
            200: ParticipantSerializer(many=True)
        },
        summary='List all participants in a competition',
        description='Retrieves a list of all participants registered in a specified competition.',
    )
    @action(detail=True, methods=['get'], url_name='participants')
    def participants(self, request, pk=None):
        competition = self.get_object() 
        participants = Participant.objects.filter(competition=competition).select_related('student_info', 'student_info__club', 'student_info__coach')
        serializer = ParticipantSerializer(participants, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve games based on optional filters",
        description="Returns a list of games associated with a competition. "
                    "The results can be further filtered by age category, weight category, and level.",
        parameters=[
            OpenApiParameter(name='age', type=OpenApiTypes.STR, required=False, description='Filter by age category'),
            OpenApiParameter(name='weight', type=OpenApiTypes.STR, required=False, description='Filter by weight category'),
            OpenApiParameter(name='level', type=OpenApiTypes.STR, required=False, description='Filter by competition level')
        ],
    )
    @action(detail=True, methods=['get'], url_name='games')
    def games(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')
        weight_category = request.query_params.get('weight')
        level = request.query_params.get('level')
        games = Game.objects.filter(competition=competition).select_related('red_corner__student_info', 'blue_corner__student_info',
                                          'red_corner__student_info__coach', 'blue_corner__student_info__coach',
                                          'red_corner__student_info__club', 'blue_corner__student_info__club').order_by('index')

        if age_category and weight_category and level:
            games = Game.objects.filter(
                    Q(age_category=age_category) & 
                    Q(weight_category=weight_category) &
                    Q(level=level) 
                )
            
        serializer = ListGameSerializer(games, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Retrieve winners for each category in a competition",
        description="This endpoint returns a list of winners for each category (age, weight) "
                    "in a given competition. Winners are those who achieved the first level in their respective categories.",
        parameters=[
            OpenApiParameter(
                name='age', 
                type=OpenApiTypes.STR, 
                required=False, 
                description='Filter winners by age category.'
            )
        ],
        responses={200: ParticipantSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_name='winners')
    def winners(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')
        participants = Participant.objects.filter(competition=competition, place=1).select_related('student_info', 'student_info__club', 'student_info__coach')
        if age_category:
            participants = Participant.objects.filter(competition=competition, place=1, age_category=age_category)
            
        serializer = ParticipantSerializer(participants, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

    @extend_schema(
        summary="Generate Tournament Brackets",
        description="Generates tournament brackets for each age and weight category.",
        responses={201: inline_serializer(
            name='GenerateTournamentBrackets',
            fields={
                'message': serializers.CharField(),
            }
            )
        },
        request=None
    )
    @action(detail=True, methods=['post'], url_name='generate_tournament_bracket')
    def generate_tournament_bracket(self, request, pk=None):
        for age, weight_categories in CATEGORIES.items():
            for weight in weight_categories:
                generate_tournament_bracket_logic(age, weight, self.get_object())
        
        return Response({"message": "Succesfully generated tournament bracket for all categories"}, status=status.HTTP_200_OK)
    

from django.db.models import Q
from rest_framework import status, viewsets, exceptions, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from game.models import Game
from game.serializers import GameSerializer, ListGameSerializer
from organizator.permissions import IsOrganizator
from .models import Competition, Participant
from .serializers import CompetitionSerializer, ParticipantSerializer, UpdateCompetitionSerializer, RegisterStudentSerializer
from .permissions import IsPresident, IsStudentCoach
from .utils import generate_tournament_bracket_logic

CATEGORIES = {
    '6-7': ['24kg', '28kg', '32kg', '36kg', '40kg', '44kg', '48kg'],
    '8-9': ['28kg', '32kg', '36kg', '40kg', '44kg', '48kg', '52kg'],
    '10-11': ['32kg', '36kg', '40kg', '44kg', '48kg', '52kg', '56kg'],
    '12-13': ['36kg', '40kg', '44kg', '48kg', '52kg', '56kg', '60kg'],
    '14-15': ['40kg', '44kg', '48kg', '52kg', '56kg', '60kg', '64kg'],
    '16-17': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg'],
}  


@extend_schema(tags=['Competition'])
class CompetitionViewsets(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
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
        examples=[
        OpenApiExample(
            name='RegisterStudentRequestExample',
            value={
                'student_id': '5af1c8df-4733-4b7d-8132-8a731503dad3',
                'age_category': '14-15',
                'weight_category': '48kg'
            },
            request_only=True,
            media_type='application/json'
        ),
        OpenApiExample(
            name='RegisterStudentExample',
            value={
                'message': 'Student registered successfully.',
                'data': {
                    'student_id': '5af1c8df-4733-4b7d-8132-8a731503dad3',
                    'age_category': '14-15',
                    'weight_category': '48kg',
                    'competition': '7bfae331-55cd-48f1-a906-3fb002e00bc0',
                    'place': None
                }
            },
            response_only=True,
            status_codes=['201'],
        )
    ],
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
        examples=[
            OpenApiExample(
                name='UnregisterStudentRequest',
                value={
                    'student_id': '5af1c8df-4733-4b7d-8132-8a731503dad3',
                },
                request_only=True,
                media_type='application/json'
            ),
            OpenApiExample(
                name='UnregisterStudentResponse',
                value={
                    'message': 'Student unregistered successfully.',
                    'data': {
                        'student_id': '5af1c8df-4733-4b7d-8132-8a731503dad3',
                    }
                },
                response_only=True,
                status_codes=['200'],
            )
        ],
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
        return Response({"message": "Student unregistered successfully.", "data": {"student_id": student_id}},
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
        participants = Participant.objects.filter(competition=competition)
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
        examples=[
            OpenApiExample(
                name='ListGames',
                value={
                    'data': [
                        {
                        'id': 'f5806108-f192-456b-b20d-0b645689234d',
                        'competition': '28fd386a-bfab-4a77-990a-cef25ebfa656',
                        'red_corner': '528052fc-3048-4576-b844-cc3cabeb795b',
                        'blue_corner': '94804990-8e92-45de-ba72-bb7b92d650d6',
                        'age_category': '14-15',
                        'weight_category': '44kg',
                        "parent": "08c50e2b-9b6a-46bf-97fc-337e55d4f2cc",
                        'level': 3,
                        'winner': None
                        }
                    ]
                },
                response_only=True,
                status_codes=['200'],
            )
        ],
    )
    @action(detail=True, methods=['get'], url_name='games')
    def games(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')
        weight_category = request.query_params.get('weight')
        level = request.query_params.get('level')
        games = Game.objects.filter(competition=competition).order_by('index')

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
        examples=[
            OpenApiExample(
                name='ListGames',
                value={
                    'data': [ {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "competition": "5af1c8df-4733-4b7d-8132-8a731503dad3",
                            "participant": "08c50e2b-9b6a-46bf-97fc-337e55d4f2cc",
                            "age_category": "14-15",
                            "weight_category": "44kg",
                            "place": 1
                        }
                    ]
                },
                response_only=True,
                status_codes=['200'],
            )
        ],
        responses={200: ParticipantSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_name='winners')
    def winners(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')
        participants = Participant.objects.filter(competition=competition, place=1)
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
    

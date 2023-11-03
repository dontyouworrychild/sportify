from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from coach.models import Coach
from competition.models import Participant
from competition.serializers import ParticipantSerializer
from game.serializers import GameSerializer
from game.models import Game
from .models import Student
from .serializers import StudentSerializer, UpdateStudentSerializer
from .permissions import IsStudentCoach, IsCoach


@extend_schema(tags=['Student'])
class StudentViewsets(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get', 'patch', 'delete']
    search_fields = ['first_name', 'last_name']

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'last_fights', 'results_in_competitions']:
            permission_classes = [AllowAny]
        if self.action in ['partial_update', 'update', 'destroy']:
            permission_classes = [IsStudentCoach]
        elif self.action in ['create']:
            permission_classes = [IsCoach]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Partially update a student's details",
        description="Updates a student's details. Only provided fields will be updated.",
        request=UpdateStudentSerializer,
        responses={
            200: inline_serializer(
                name='UpdateStudentInfo',
                fields={
                    'message': 'Student updated successfully',
                    'data': UpdateStudentSerializer()
                }
            )
        },
    )
    def partial_update(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = UpdateStudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Student updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def create(self, request):
        coach_id = self.request.user.id
        try:
            coach = Coach.objects.get(id=coach_id)
            student_data = {
                    'location': coach.location,
                    'sport_type': coach.sport_type,
                    'club': coach.club_id,
                    'coach': coach_id,
                    **request.data
                }
            serializer = self.get_serializer(data=student_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Coach.DoesNotExist:
                return Response({"error": "Invalid coach ID."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
    summary='Retrieve Last Fights of a Student',
    description='Fetches a list of the most recent fights for a given student, organized by competition start date.',
    examples=[
            OpenApiExample(
                name='RetrieveLastFightsOfStudent',
                summary='Retrieve a list of the most recent fights for a given student',
                value={
                    "data": [
                        [ 
                            {
                                "id": "0ea55364-7acf-443b-b259-1fd84e83dfee",
                                "competition": "7bfae331-55cd-48f1-a906-3fb002e00bc0",
                                "red_corner": None,
                                "blue_corner": "3797a702-f655-4f6f-9a69-32623ff3c61e",
                                "parent": "44b6cb7b-f0d2-41bf-82e9-f9ca404f81f1",
                                "age_category": "12-13",
                                "weight_category": "48kg",
                                "winner": "3797a702-f655-4f6f-9a69-32623ff3c61e",
                                "level": 3
                            },
                            {
                                "id": "44b6cb7b-f0d2-41bf-82e9-f9ca404f81f1",
                                "competition": "7bfae331-55cd-48f1-a906-3fb002e00bc0",
                                "red_corner": "a5843a7f-59cd-4235-b4d5-4510627a9018",
                                "blue_corner": "3797a702-f655-4f6f-9a69-32623ff3c61e",
                                "parent": "53146ca6-905c-45c0-babc-7c15558cf4f2",
                                "age_category": "12-13",
                                "weight_category": "48kg",
                                "winner": "a5843a7f-59cd-4235-b4d5-4510627a9018",
                                "level": 2
                            },
                        ],
                        [ 
                            {
                                "id": "eeaa7b1b-3fab-4e3b-b17f-4155063bc7b9",
                                "competition": "5af1c8df-4733-4b7d-8132-8a731503dad3",
                                "red_corner": "3797a702-f655-4f6f-9a69-32623ff3c61e",
                                "blue_corner": "830d5a7c-4817-416b-9246-b062b74e89da",
                                "parent": "44b6cb7b-f0d2-41bf-82e9-f9ca404f81f1",
                                "age_category": "12-13",
                                "weight_category": "48kg",
                                "winner": "830d5a7c-4817-416b-9246-b062b74e89da",
                                "level": 2
                            }
                        ],
                    ]
                },
                response_only=True,
                status_codes=['200'],
            )
        ]
    )
    @action(detail=True, methods=['get'], url_name='last-fights')
    def last_fights(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(participant=student).order_by('competition__start_date')
        games = []
        for participant in participants:
            current_games = Game.objects.filter(Q(red_corner=participant) | Q(blue_corner=participant)).order_by('-level')
            games_for_participant = []
            for current_game in current_games:
                games_for_participant.append(current_game)

            serializer = GameSerializer(games_for_participant, many=True)
            games.append(serializer.data)
        return Response({"data": games}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Get Competition Results of a Student",
        description="Retrieves a list of competitions and the corresponding results for a given student, "
                    "ordered by the start date of the competitions.",
        examples=[
        OpenApiExample(
            name='GetResultsInCompetitions',
            value={
                'data': [{
                    'student_id': '5af1c8df-4733-4b7d-8132-8a731503dad3',
                    'competition': '7bfae331-55cd-48f1-a906-3fb002e00bc0',
                    'participant': '1c285a1d-e5a1-4cf1-8902-a16292002e81',
                    'age_category': '14-15',
                    'weight_category': '48kg',
                    'place': 2
                }]
            },
            response_only=True,
            status_codes=['200'],
        )
    ],
    )
    @action(detail=True, methods=['get'], url_name='results-in-competitions')
    def results_in_competitions(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(participant=student).order_by('competition__start_date')
        serializer = ParticipantSerializer(participants, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
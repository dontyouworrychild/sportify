from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from coach.models import Coach
from competition.models import Participant
from competition.serializers import ParticipantSerializer, StudentResultsInCompetitionsSerializer
from game.serializers import GameSerializer
from game.models import Game
from .models import Student
from .serializers import StudentSerializer, UpdateStudentSerializer, StudentProfileSerializer, CreateStudentSerializer, RequestCreateStudentSerializer
from .permissions import IsStudentCoach, IsCoach
# from game.serializers import ListStudentLastGamesSerializer
from competition.serializers import ListNameCompetitionSerializer
from game.serializers import StudentLastGamesModelGameSerializer
# from .serializers import StudentResultsInCompetitionsSerializer
# from competition.serializers import StudentResultsInCompetitionsSerializer

@extend_schema(tags=['Student'])
class StudentViewsets(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get', 'patch', 'delete']
    search_fields = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action in ['create']:
            return RequestCreateStudentSerializer
        return StudentProfileSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'last_fights', 'results_in_competitions']:
            permission_classes = [AllowAny]
        if self.action in ['partial_update', 'update', 'destroy']:
            permission_classes = [IsStudentCoach]
        elif self.action in ['create', 'my_students']:
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
            # student_data = {key: value[0] for key, value in request.data.lists()}
            student_data = {key: value[0] if isinstance(value, list) else value for key, value in request.data.items()}
            student_data['location'] = coach.location
            student_data['club'] = coach.club_id
            student_data['coach'] = coach.id
            # print(student_data)
            serializer = CreateStudentSerializer(data=student_data)
            # serializer = self.get_serializer(data=student_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Coach.DoesNotExist:
                return Response({"error": "Invalid coach ID."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
    summary='Retrieve Last Fights of a Student',
    description='Fetches a list of the most recent fights for a given student, organized by competition start date.',
    )
    @action(detail=True, methods=['get'], url_name='last_fights')
    def last_fights(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(student_info=student).order_by('competition__start_date')
        
        competitions_games = {}
        for participant in participants:
            competition = participant.competition
            if competition.id not in competitions_games:
                competitions_games[competition.id] = {
                    "competition": competition,
                    "games": []
                }

            current_games = Game.objects.filter(Q(red_corner=participant) | Q(blue_corner=participant)).order_by('-level')
            for current_game in current_games:
                competitions_games[competition.id]["games"].append(current_game)

        results = []
        for comp_id, data in competitions_games.items():
            games_serializer = StudentLastGamesModelGameSerializer(data["games"], many=True, context={'student_id': student.id})
            competition_serializer = ListNameCompetitionSerializer(data["competition"])
            results.append({
                "competition": competition_serializer.data,
                "games": games_serializer.data
            })

        return Response({"data": results}, status=status.HTTP_200_OK)

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
    @action(detail=True, methods=['get'], url_name='results_in_competitions')
    def results_in_competitions(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(student_info=student, place__isnull=False).order_by('competition__start_date')
        # games = Game.objects.filter(Q(red_corner__in=participants) | Q(blue_corner__in=participants)).order_by('-level')
        serializer = StudentResultsInCompetitionsSerializer(participants, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        """
        Optionally restricts the returned students to a given coach,
        by filtering against a `coach` query parameter in the URL.
        """
        queryset = Student.objects.all()
        coach_username = self.request.query_params.get('coach')
        club_name = self.request.query_params.get('club')

        if coach_username is not None:
            coach = get_object_or_404(Coach, username=coach_username)
            queryset = queryset.filter(coach=coach)

        if club_name:
            # Adjust this line if the lookup field for the club is different in your model.
            queryset = queryset.filter(club__name=club_name)

        return queryset
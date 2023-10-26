from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from competition.models import Competition, Participant
from competition.serializers import ParticipantSerializer
from game.serializers import GameSerializer
from game.models import Game
from django.db.models import Q

from .models import Student
from coach.models import Coach
from .serializers import StudentSerializer
from .permissions import IsStudentCoach, IsCoach
from rest_framework.decorators import action

from django.db.models import F


class StudentViewsets(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'list_last_fights', 'results_in_competitions']:
            permission_classes = [AllowAny]
        if self.action in ['partial_update', 'update', 'destroy']:
            permission_classes = [IsStudentCoach]
        elif self.action in ['create']:
            permission_classes = [IsCoach]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        if self.request.user.is_authenticated:
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
        else:
            return Response({"error": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=True, methods=['get'], url_name='list_last_fights')
    def list_last_fights(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(participant=student).order_by('competition__start_date')
        games = []
        for participant in participants:
            current_games = Game.objects.filter(Q(red_corner=participant) | Q(blue_corner=participant)).order_by('-level')
            for current_game in current_games:
                games.append(current_game)

        serializer = GameSerializer(games, many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_name='results_in_competitions')
    def results_in_competitions(self, request, pk=None):
        student = self.get_object()
        participants = Participant.objects.filter(participant=student).order_by('competition__start_date')
        serializer = ParticipantSerializer(participants, many=True)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
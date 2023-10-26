from rest_framework import status, viewsets, exceptions
from django.db.models import Q
from .models import Competition, Participant
from game.models import Game
from .serializers import CompetitionSerializer, ParticipantSerializer
from game.serializers import GameSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsPresident, IsOrganizator, IsStudentCoach
from rest_framework.response import Response
from rest_framework.decorators import action
from student.models import Student

import math

CATEGORIES = {
    '6-7': ['24kg', '28kg', '32kg', '36kg', '40kg', '44kg', '48kg'],
    '8-9': ['28kg', '32kg', '36kg', '40kg', '44kg', '48kg', '52kg'],
    '10-11': ['32kg', '36kg', '40kg', '44kg', '48kg', '52kg', '56kg'],
    '12-13': ['36kg', '40kg', '44kg', '48kg', '52kg', '56kg', '60kg'],
    '14-15': ['40kg', '44kg', '48kg', '52kg', '56kg', '60kg', '64kg'],
    '16-17': ['44kg', '48kg', '52kg', '56kg', '60kg', '64kg', '68kg'],
}  


class CompetitionViewsets(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsPresident]
        elif self.action in ['partial_update']:
            permission_classes = [IsOrganizator, IsPresident]
        elif self.action in ['register_student']:
            permission_classes = [IsStudentCoach]
        elif self.action in ['retrieve', 'list', 'list_participants', 'generate_tournament_bracket_for_all', 'list_games', 'get_winners']:
            # generate_tournament_bracket - udalit' etu kerek
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check if the user is an "organizator"
        if request.user.role == 'organizator':
            allowed_fields = {'start_date', 'end_date', 'address'}
            for field in set(serializer.fields) - allowed_fields:
                if field in request.data:
                    return Response({"error": f"Organizators can only update start_date, end_date, and address fields."},
                                    status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='register_student')
    def register_student(self, request, pk=None):
        competition = self.get_object()  # Get the competition instance
        
        student_id = request.data.get('student_id', None)
        
        if not student_id:
            raise exceptions.ValidationError("Please provide student_id in the request data.")

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            raise exceptions.NotFound("Student with the provided ID does not exist.")
        
        if competition.participants.filter(participant=student).exists():
            raise exceptions.ValidationError("Student is already registered for this competition.")
    
        age_category = request.data.get('age_category')
        weight_category = request.data.get('weight_category')


        if age_category not in CATEGORIES:
            return Response({"error": "Invalid age category for this competition."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if weight_category not in CATEGORIES[age_category]:
            return Response({"error": "Invalid weight category for this competition."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create a Participant instance
        Participant.objects.create(
            participant=student,
            competition=competition,
            age_category=request.data.get('age_category'),
            weight_category=request.data.get('weight_category')
        )
        
        return Response({"message": "Student registered successfully."},
                        status=status.HTTP_201_CREATED)
        
    
    @action(detail=True, methods=['post'], url_path='unregister_student')
    def unregister_student(self, request, pk=None):
        competition = self.get_object()  # Get the competition instance
        
        # Assuming the student is passed in the request data
        student_id = request.data.get('student_id', None)
        
        if not student_id:
            raise exceptions.NotFound("Student with the provided ID does not exist.")
        
        try:
            participant = Participant.objects.get(participant_id=student_id, competition=competition)
        except Participant.DoesNotExist:
            return Response({"error": "Student is not registered for this competition."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the Participant instance
        participant.delete()
        
        return Response({"message": "Student unregistered successfully."},
                        status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_name='list_participants')
    def list_participants(self, request, pk=None):
        competition = self.get_object()
        participants = Participant.objects.filter(competition=competition)
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='list_games')
    def list_games(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')
        weight_category = request.query_params.get('weight')
        level = request.query_params.get('level')
        
        games = Game.objects.filter(competition=competition)

        if age_category and weight_category and level:
            games = Game.objects.filter(
                    Q(age_category=age_category) & 
                    Q(weight_category=weight_category) &
                    Q(level=level) 
                )
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['get'], url_name='get_winners')
    def get_winners(self, request, pk=None):
        competition = self.get_object()
        age_category = request.query_params.get('age')

        games = Game.objects.filter(competition=competition, level=1)
        if age_category:
            games = Game.objects.filter(competition=competition, age_category=age_category, level=1)

        winners = [game.winner for game in games if game.winner is not None]
        
        serializer = ParticipantSerializer(winners, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def nextPowerOf2(self, length):
        # Calculate log2 of N
        if (length < 1):
            return 0
        a = math.log2(length)
        a = int(a)
 
        if 2**a == length:
            return length
    
        return 2**(a + 1)

    @action(detail=True, methods=['post'], url_name='generate_tournament_bracket_for_all')
    def generate_tournament_bracket_for_all(self, request, pk=None):

        for age, weight_categories in CATEGORIES.items():
            for weight in weight_categories:
                self.generate_tournament_bracket(age, weight)
        
        return Response({"message": "Succesfully generated tournament bracket for all categories"}, status=status.HTTP_200_OK)
    
    def generate_tournament_bracket(self, age_category, weight_category):
        competition = self.get_object()
        participants = list(Participant.objects.filter(competition=competition, age_category=age_category, weight_category=weight_category))

        next_power_of_two = self.nextPowerOf2(len(participants))

        if next_power_of_two < 1:
            return "There are no participants"

        while len(participants) < next_power_of_two:
            participants.append(None)

        # normalize tut, sorting anau-mynau osynda bolu kerek
        return self.generate_tournament_bracket_for_individual_category(participants=participants, age_category=age_category, weight_category=weight_category)
        
        
    def generate_tournament_bracket_for_individual_category(self, participants, age_category, weight_category):
    
        level = math.log2(len(participants))
        max_level = level
        prev_level = []
        current_level = []

        if len(participants) == 0:
            return Response({"message": "No games in {age_category} - {weight_category}"}, status=status.HTTP_200_OK)
        
        if len(participants) == 1:
            g =  Game(competition=self.get_object(),
                 blue_corner=participants[0], red_corner=None,
                 age_category=age_category, weight_category=weight_category
                 )
            g.save()
            return Response({"message": "Succesfully generated tournament bracket for single participant"}, status=status.HTTP_200_OK)
        
        index = 1
        
        for i in range(int(len(participants) / 2)):
            player1_id = i
            player2_id = len(participants) - 1 - i

            if participants[player2_id] is None:
                g = Game(competition=self.get_object(),
                         blue_corner=participants[player1_id], red_corner=None,
                         age_category=age_category, weight_category=weight_category, level=level, index=index)
                g.save()
                index += 1
                prev_level.append(g)
            else:
                g = Game(competition=self.get_object(),
                         blue_corner=participants[player1_id], red_corner=participants[player2_id],
                         age_category=age_category, weight_category=weight_category, level=level, index=index)
                g.save()
                index += 1
                prev_level.append(g)
        
        level -= 1

        while level >= 1:
            for i in range(0, len(prev_level), 2):
                if level + 1 == max_level:
                    if prev_level[i].red_corner is None:
                        prev_level[i].winner = prev_level[i].blue_corner
                    if prev_level[i + 1].red_corner is None:
                        prev_level[i + 1].winner = prev_level[i + 1].blue_corner
                
                g = Game(competition=self.get_object(),
                         blue_corner=prev_level[i].winner, red_corner=prev_level[i+1].winner,
                         age_category=age_category, weight_category=weight_category, level=level, index=index)
                index += 1

                g.save()
                
                prev_level[i].parent = g
                prev_level[i].save()
                prev_level[i+1].parent = g
                prev_level[i+1].save()
                current_level.append(g)
            
            prev_level = current_level
            current_level = []
            
            level -= 1


        return Response({"message": "Succesfully generated tournament bracket"}, status=status.HTTP_200_OK)
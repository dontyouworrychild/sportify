from collections import deque
from rest_framework import filters, status, viewsets, exceptions
from django.db.models import Q
from common.enums import SystemRoleEnum
from .models import Competition, Participant, Game
from .serializers import CompetitionSerializer, ParticipantSerializer, GameSerializer, ListGameSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsPresident, IsOrganizator, IsStudentCoach
from rest_framework.response import Response
from rest_framework.decorators import action
from student.models import Student

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
        elif self.action in ['retrieve', 'list', 'list_participants', 'generate_tournament_bracket_for_all', 'list_games']:
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
        
        games = Game.objects.filter(competition=competition)

        if age_category and weight_category:
            games = Game.objects.filter(
                    Q(age_category=age_category) & 
                    Q(weight_category=weight_category) 
                )
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    # @action(detail=True, methods=['get'], url_name='list_games')
    # def list_games(self, request, pk=None):
    #     competition = self.get_object()
    #     games = Game.objects.filter(competition=competition)
    #     max_lvl = 0
    #     for game in games:
    #         max_lvl = max(max_lvl, game.level)

    #     # q = deque(Game)
    #     # q.append(games[0])
    #     q = deque(Game)
    #     q.append(games[0])


    #     gamesList = list(Game)
    #     while q.count > 0:
    #         game = q[0]
    #         gamesList.append(game)

    #         if game.fighter1 != None:
    #             q.append(game.fighter1)
    #         if game.fighter2 != None:
    #             q.append(game.fighter2)
    #         if game.fighter1 == None and game.level != max_lvl:
    #             q.append(Game())
    #         if game.fighter2 != None and game.level != max_lvl:
    #             q.append(Game())
            
    #         q.popleft()
    #     gamesList.reverse()
    #     serializer = ListGameSerializer(gamesList, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='generate_tournament_bracket_for_all')
    def generate_tournament_bracket_for_all(self, request, pk=None):

        for age, weight_categories in CATEGORIES.items():
            for weight in weight_categories:
                self.generate_tournament_bracket(age, weight)
        
        return Response({"message": "Generated tournament for all the categories"}, status=status.HTTP_200_OK)
    
    # @action(detail=True, methods=['post'], url_name='generate_tournament_bracket')
    def generate_tournament_bracket(self, age_category, weight_category):
        competition = self.get_object()
        participants = Participant.objects.filter(competition=competition, age_category=age_category, weight_category=weight_category)

        # normalize tut, sorting anau-mynau osynda bolu kerek

        self.generate_tournament_bracket_for_individual_category(participants=participants, age_category=age_category, weight_category=weight_category)
        
    def generate_tournament_bracket_for_individual_category(self, participants, age_category, weight_category):
        def divide(start, end):
            if end < start:
                return
            if end - start == 1:
                fight = Game(competition=self.get_object(), 
                             blue_corner=participants[start], red_corner=participants[end], 
                             empty=False, age_category=age_category, weight_category=weight_category)
                fight.save()
                return fight
            if end == start:
                fight = Game(competition=self.get_object(), 
                             red_corner=participants[end], empty=True,
                             age_category=age_category, weight_category=weight_category)
                fight.save()
                return fight
                    
            mid = (end - start) // 2

            fight = Game(competition=self.get_object(), 
                         age_category=age_category, weight_category=weight_category)
            fight.save()
            first_fight = divide(start, start + mid)
            first_fight.parent_id = fight.id
            first_fight.save() 
            second_fight = divide(start + mid + 1, end)
            second_fight.parent_id = fight.id
            second_fight.save() 

            return fight

        divide(0, len(participants) - 1)
        return Response({"message": "Succesfully generated tournament bracket"}, status=status.HTTP_200_OK)
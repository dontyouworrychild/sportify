from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from competition.models import Participant
from .models import Game
from .serializers import GameSerializer, SelectWinnerSerializer, ListGameSerializer
from .permissions import IsCompetitionOrganizator

@extend_schema(tags=['Game'])
class GameViewsets(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['select_winner']:
            permission_classes = [IsCompetitionOrganizator]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Disable Creation of New Games",
        description="Prevents the creation of new Game instances via POST request.",
        request=None,
        responses={
            405: OpenApiExample(
                "Method Not Allowed",
                summary="Creation of new games via POST is not allowed",
                description="This response is returned when a POST request is made attempting to create a new Game instance.",
                value={"error": "Creation of new games via POST is not allowed."},
                response_only=True,
                status_codes=["405"],
            )
        },
        examples=[
            OpenApiExample(
                name='DisablePostGame',
                value={
                    "error": "Creation of new games via POST is not allowed."
                },
                response_only=True,
                media_type='application/json',
                status_codes=['405']
            ),
        ]
    )
    def create(self):
        """
        Override the create method to disable POST requests for creating a new Game.
        """
        return Response({"error": "Creation of new games via POST is not allowed."}, 
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(
        summary="Select a Winner for a Game",
        description="Allows the selection of a winner for a specific game. "
                    "The winner is identified by their participant ID.",
        request=SelectWinnerSerializer,
        responses={
            200: inline_serializer(
            name='SelectWinnerResponse',
            fields={
                'message': "Winner selected successfully",
                'data': GameSerializer()
            }
        )
        },
    )
    @action(detail=True, methods=['post'], url_name='select-winner')
    def select_winner(self, request, pk=None):
        game = self.get_object()

        try:
            winner = self.get_participant(request.data.get('winner'))
        except Participant.DoesNotExist:
            return Response({"error": "Sorry there is no participant with that id"}, status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_winner(game, winner):
            return Response({"error": "Sorry, invalid participant selection"}, status=status.HTTP_400_BAD_REQUEST)

        self.update_winner(game, winner)
        game_serializer = ListGameSerializer(game)
        return Response({"message": "Winner selected successfully", "data": game_serializer.data}, status=status.HTTP_200_OK)

    def get_participant(self, participant_id):
        if not participant_id:
            raise Participant.DoesNotExist
        return Participant.objects.get(id=participant_id)

    def is_valid_winner(self, game, winner):
        return winner in [game.blue_corner, game.red_corner]

    def update_winner(self, game, winner):
        self.update_game(game, winner)
        self.assign_losers_ranking(game)
        self.update_parent_game(game, winner)

    def update_game(self, game, winner):
        data = {}
        if winner == game.red_corner:
            data['red_corner_winner'] = True
        elif winner == game.blue_corner:
            data['blue_corner_winner'] = True

        serializer = SelectWinnerSerializer(game, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def assign_losers_ranking(self, game):
        loser = None
        if game.red_corner_winner:
            loser = game.blue_corner
        elif game.blue_corner_winner:
            loser = game.red_corner
        
        if loser:
            loser.place = 2 ** (game.level - 1) + 1
            loser.save()

    def update_parent_game(self, game, winner):
        if game.parent is not None:
            if not game.parent.blue_corner:
                game.parent.blue_corner = winner
            elif not game.parent.red_corner:
                game.parent.red_corner = winner
            game.parent.save()
        else:
            # If the game does not have parent, then it means it is a final, and the winner should have place = 1
            winner.place = 1
            winner.save()




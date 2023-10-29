from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from competition.models import Participant
from .models import Game
from .serializers import GameSerializer, UpdateGameSerializer
from .permissions import IsCompetitionOrganizator

@extend_schema(tags=['Game'])
class GameViewsets(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    # permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['partial_update', 'select_winner']:
            permission_classes = [IsCompetitionOrganizator]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'], url_name='select-winner')
    def select_winner(self, request, pk=None):
        game = self.get_object()

        winner = Participant.objects.get(id=request.data['winner'])
        if winner is None:
            return Response({"error": "Sorry there is no participant with that id"}, status=status.HTTP_400_BAD_REQUEST)
        
        if winner not in [game.blue_corner, game.red_corner]:
            return Response({"error": "sorry brat"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UpdateGameSerializer(game, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if game.red_corner is not None and game.red_corner != game.winner:
            game.red_corner.place = 2 ** (game.level - 1) + 1
            game.red_corner.save()
        if game.blue_corner is not None and game.blue_corner != game.winner:
            game.blue_corner.place = 2 ** (game.level - 1) + 1
            game.blue_corner.save()
        

        if game.parent is not None:
            if game.parent.red_corner in [game.red_corner, game.blue_corner]:
                game.parent.red_corner = game.winner
            elif game.parent.blue_corner in [game.red_corner, game.blue_corner]:
                game.parent.blue_corner = game.winner
            elif game.parent.red_corner is None:
                game.parent.red_corner = game.winner
            elif game.parent.blue_corner is None:
                game.parent.blue_corner = game.winner
            game.parent.save()
        else:
            game.place = 1
            game.save()

        return Response({"message": serializer.data}, status=status.HTTP_200_OK)




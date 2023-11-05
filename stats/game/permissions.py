from django.shortcuts import get_object_or_404
from rest_framework import permissions
from common.enums import SystemRoleEnum
from .models import Game


class IsCompetitionOrganizator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.role != SystemRoleEnum.ORGANIZATOR:
            return False

        game_id = view.kwargs.get('pk')

        game = get_object_or_404(Game, id=game_id)

        '''
        Негизи осындай линия болу керек, когда modelкада, ArrayField сиакты ма болса organizatorsка
        if request.user in game.competition.organizators:
            return True
        '''
        if request.user.id == game.competition.organizator.id:
            return True

        return False
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Club
from .serializers import ClubSerializer


class ClubViewsets(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'list']
    
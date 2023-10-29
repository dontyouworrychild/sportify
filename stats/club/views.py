from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Club
from .serializers import ClubSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Club'])
class ClubViewsets(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'list']
    
    
    def get(self, request, *args, **kwargs):
        """Retrieves information about a specific club based on unique identifier (uuid)"""
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """Lists all clubs"""
        return super().list(request, *args, **kwargs)
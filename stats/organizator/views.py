from rest_framework.permissions import AllowAny
from user.views import UserViewsets
from .models import Organizator
from .serializers import OrganizatorSerializer, UpdateOrganizatorSerializer
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOrganizator


class OrganizatorViewsets(UserViewsets):
    queryset = Organizator.objects.all()
    serializer_class = OrganizatorSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'patch']
    
    def get_permissions(self):
        if self.action in ['partial_update']:
            permission_classes = [IsOrganizator]
        elif self.action in ['get', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, pk=None):
        organizator = self.get_object()
        if organizator.image:
            organizator.delete_image()
        serializer = UpdateOrganizatorSerializer(organizator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from user.views import UserViewsets
from .models import Organizator
from .serializers import OrganizatorSerializer, UpdateOrganizatorSerializer
from .permissions import IsMe

@extend_schema(tags=['Organizator'])
class OrganizatorViewsets(UserViewsets):
    queryset = Organizator.objects.all()
    serializer_class = OrganizatorSerializer
    # permission_classes = [AllowAny]
    http_method_names = ['get', 'patch', 'post']
    
    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['partial_update']:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, pk=None):
        organizator = self.get_object()
        if organizator.image:
            organizator.delete_image()
        serializer = UpdateOrganizatorSerializer(organizator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Image updated successfully"}, status=status.HTTP_200_OK)
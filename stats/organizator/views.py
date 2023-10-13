from rest_framework.permissions import AllowAny
from user.views import UserViewsets
from .models import Organizator
from .serializers import OrganizatorSerializer


class OrganizatorViewsets(UserViewsets):
    queryset = Organizator.objects.all()
    serializer_class = OrganizatorSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'list']
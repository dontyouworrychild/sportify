from rest_framework.permissions import AllowAny
from user.views import UserViewsets
from .models import Coach
from .serializers import CoachSerializer


class CoachViewsets(UserViewsets):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'list']
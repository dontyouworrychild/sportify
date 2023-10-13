from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Student
from coach.models import Coach
from .serializers import StudentSerializer
from .permissions import IsStudentCoach, IsCoach


class StudentViewsets(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permission_classes = [AllowAny]
        if self.action in ['partial_update', 'update', 'destroy']:
            permission_classes = [IsStudentCoach]
        elif self.action in ['create']:
            permission_classes = [IsCoach]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        if self.request.user.is_authenticated:
            coach_id = self.request.user.id
            try:
                coach = Coach.objects.get(id=coach_id)

                student_data = {
                    'location': coach.location,
                    'sport_type': coach.sport_type,
                    'club': coach.club_id,
                    'coach': coach_id,
                    **request.data
                }

                serializer = self.get_serializer(data=student_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Coach.DoesNotExist:
                return Response({"error": "Invalid coach ID."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
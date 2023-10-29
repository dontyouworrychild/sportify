from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from student.models import Student
from student.serializers import StudentSerializer
from user.views import UserViewsets
from .models import Coach
from .serializers import CoachSerializer, UpdateCoachSerializer
from .permissions import IsMe


@extend_schema(tags=['Coach'])
class CoachViewsets(UserViewsets):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    http_method_names = ['get', 'list', 'patch']

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['partial_update']:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]
    
    def partial_update(self, request, pk=None):
        """
        Partially updates a Coach model's 'image' field. 
        It allows you to remove an existing image associated with a coach and replace it with a new one. 
        """
        coach = self.get_object()
        if coach.image:
            coach.delete_image()
        serializer = UpdateCoachSerializer(coach, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Image updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='students')
    def students(self, request, pk=None):
        """
        Retrieves a list of students associated with a coach based on the unique identifier (ID) of the coach. 
        It allows you to view the students who are under the guidance of a specific coach
        """
        coach = self.get_object()
        students = Student.objects.filter(coach=coach)
        serializer = StudentSerializer(students, many=True)
        
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)
    

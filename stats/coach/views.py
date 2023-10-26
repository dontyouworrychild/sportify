from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from student.models import Student
from student.serializers import StudentSerializer
from user.views import UserViewsets
from .models import Coach
from .serializers import CoachSerializer


class CoachViewsets(UserViewsets):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'list']
    

    @action(detail=True, methods=['get'], url_name='students')
    def students(self, request, pk=None):
        coach = self.get_object()
        students = Student.objects.filter(coach=coach)
        serializer = StudentSerializer(students, many=True)
        
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)

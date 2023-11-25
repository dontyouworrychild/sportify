from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, inline_serializer
from student.models import Student
from student.serializers import StudentSerializer
from user.views import UserViewsets
from .models import Coach
from .serializers import CoachSerializer, UpdateCoachSerializer, CoachPageSerializer
from .permissions import IsMe


@extend_schema(tags=['Coach'])
class CoachViewsets(UserViewsets):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    http_method_names = ['get', 'patch']

    def list(self, request, *args, **kwargs):
        coaches = Coach.objects.all()
        serializer = CoachPageSerializer(coaches, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action in ['partial_update']:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Update Coach Image",
        description="Partially updates a Coach model's 'image' field. This endpoint allows for the removal of an existing image "
                    "associated with a coach and replaces it with a new one.",
        request=UpdateCoachSerializer,
        responses={
            200: inline_serializer(
                name='UpdateCoachResponse',
                fields={
                    'message': 'Image updated successfully',
                    'data': UpdateCoachSerializer()
                }
            ),
        }
    )
    def partial_update(self, request, pk=None):
        coach = self.get_object()
        if coach.image:
            coach.delete_image()
        serializer = UpdateCoachSerializer(coach, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Image updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve Students by Coach",
        description="Retrieves a list of students associated with a coach based on the unique identifier (ID) of the coach. "
                    "This endpoint allows users to view the students who are under the guidance of a specific coach.",
        responses={
            200: inline_serializer(
                name='StudentListResponse',
                fields={
                    'data': serializers.ListField(child=StudentSerializer())
                }
            ),
        }
    )
    @action(detail=True, methods=['get'], url_name='students')
    def students(self, request, pk=None):
        coach = self.get_object()
        students = Student.objects.filter(coach=coach)
        serializer = StudentSerializer(students, many=True)
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

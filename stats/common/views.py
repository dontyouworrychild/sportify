from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from student.serializers import StudentSerializer
from coach.models import Coach
from coach.serializers import CoachSerializer
from club.models import Club
from club.serializers import ClubSerializer

class GlobalSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('search', '')
        if not query:
            return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search in Students
        students = Student.objects.filter(first_name__icontains=query) | Student.objects.filter(last_name__icontains=query)
        student_serializer = StudentSerializer(students, many=True)

        # Search in Coaches
        coaches = Coach.objects.filter(first_name__icontains=query) | Coach.objects.filter(last_name__icontains=query)
        coach_serializer = CoachSerializer(coaches, many=True)
        
        # Search in Clubs
        clubs = Club.objects.filter(name__icontains=query)
        club_serializer = ClubSerializer(clubs, many=True)
        
        # Combine Results
        results = {
            'students': student_serializer.data,
            'coaches': coach_serializer.data,
            'clubs': club_serializer.data,
        }
        return Response(results, status=status.HTTP_200_OK)

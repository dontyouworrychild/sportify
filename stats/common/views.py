from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from student.models import Student
from student.serializers import StudentSerializer
from coach.models import Coach
from coach.serializers import CoachSerializer
from club.models import Club
from club.serializers import ClubSerializer
from competition.models import Region
from competition.serializers import RegionSerializer
from drf_spectacular.utils import extend_schema
from .serializers import GlobalSearchResultsSerializer

class GlobalSearchAPIView(GenericAPIView):
    serializer_class = GlobalSearchResultsSerializer
    def get(self, request):
        query = request.query_params.get('search', '')
        if not query:
            return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search in Students
        students = Student.objects.filter(first_name__istartswith=query) | Student.objects.filter(last_name__istartswith=query)

        # Search in Coaches
        coaches = Coach.objects.filter(first_name__istartswith=query) | Coach.objects.filter(last_name__istartswith=query)        
        # Search in Clubs
        clubs = Club.objects.filter(name__istartswith=query)
        
        # Combine Results
        serializer = GlobalSearchResultsSerializer({
            'students': students,
            'coaches': coaches,
            'clubs': clubs,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(tags=['Region'])
class RegionAPIView(APIView):
    queryset = Region
    http_method_names = ['get']
    serializer_class = RegionSerializer

    @extend_schema(
        summary='List all regions',
        description='List all Kazakhstan\'s regions and republic cities (Astana, Shymkent, Almaty)'
    )
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
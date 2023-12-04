from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from coach.models import Coach
from club.models import Club
from competition.models import Region, Federation
from competition.serializers import RegionSerializer, ListFederationSerializer
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
    http_method_names = ['get', 'post']
    serializer_class = RegionSerializer

    @extend_schema(
        summary='List all regions',
        description='List all Kazakhstan\'s regions and republic cities (Astana, Shymkent, Almaty)'
    )
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary='Create a new region',
        description='Add a new region to Kazakhstan\'s regions and republic cities'
    )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(tags=['Federation'])
class FederationAPIView(APIView):
    queryset = Federation
    http_method_names = ['get', 'post']
    serializer_class = ListFederationSerializer

    @extend_schema(
        summary='List all federations',
    )
    def get(self, request):
        regions = Federation.objects.all()
        serializer = ListFederationSerializer(regions, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary='Create a new federation',
    )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


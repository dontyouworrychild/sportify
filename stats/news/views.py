from rest_framework import viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample
from .models import News
from .serializers import NewsSerializer

@extend_schema(tags=['News'])
class NewsViewsets(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    http_method_names = ['get']


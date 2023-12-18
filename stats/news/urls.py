from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsViewsets

app_name = 'news'

router = DefaultRouter()
router.register('', NewsViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
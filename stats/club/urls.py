from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClubViewsets

app_name = 'club'

router = DefaultRouter()
router.register('', ClubViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
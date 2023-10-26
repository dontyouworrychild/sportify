from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GameViewsets

app_name = 'game'

router = DefaultRouter()
router.register('', GameViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
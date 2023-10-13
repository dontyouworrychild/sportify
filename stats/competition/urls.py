from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompetitionViewsets

app_name = 'competition'

router = DefaultRouter()
router.register('', CompetitionViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CoachViewsets

app_name = 'coach'

router = DefaultRouter()
router.register('', CoachViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
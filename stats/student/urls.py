from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentViewsets

app_name = 'student'

router = DefaultRouter()
router.register('', StudentViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
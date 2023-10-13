from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrganizatorViewsets

app_name = 'organizator'

router = DefaultRouter()
router.register('', OrganizatorViewsets)

urlpatterns = [
    path('', include(router.urls)),
]
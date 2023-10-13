from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user.urls.auth')),
    path('api/v1/users/', include('user.urls.user')),
    path('api/v1/organizators/', include('organizator.urls')),
    path('api/v1/competitions/', include('competition.urls')),
    path('api/v1/students/', include('student.urls')),
    path('api/v1/coaches/', include('coach.urls')),
    path('api/v1/clubs/', include('club.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
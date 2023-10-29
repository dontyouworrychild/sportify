from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user.urls.auth')),
    path('api/v1/users/', include('user.urls.user')),
    path('api/v1/organizators/', include('organizator.urls')),
    path('api/v1/competitions/', include('competition.urls')),
    path('api/v1/students/', include('student.urls')),
    path('api/v1/coaches/', include('coach.urls')),
    path('api/v1/clubs/', include('club.urls')),
    path('api/v1/games/', include('game.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
# #    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]
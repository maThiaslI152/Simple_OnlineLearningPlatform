from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from user.token_views import CustomTokenObtainPairView
from core.views import FileUploadTestView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',   include('user.urls')), 
    path('api/', include('course.urls')),
    path('api/upload/', FileUploadTestView.as_view(), name='upload-test'),
    # 1) JSON schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # 2) Swagger UI
    path(
      'api/schema/swagger-ui/',
      SpectacularSwaggerView.as_view(url_name='schema'),
      name='swagger-ui'
    ),

    # 3) ReDoc (optional)
    path(
      'api/schema/redoc/',
      SpectacularRedocView.as_view(url_name='schema'),
      name='redoc'
    ),
]
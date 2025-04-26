from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from user.token_views import CustomTokenObtainPairView
from core.views import FileUploadTestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',   include('user.urls')), 
    path('api/', include('course.urls')),
    path('api/upload/', FileUploadTestView.as_view(), name='upload-test'),
]
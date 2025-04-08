from django.urls import path, include
from django.http import JsonResponse

urlpatterns = [
    path('auth/test/', lambda request: JsonResponse({"status": "ok"})),
    path('auth/' , include('dj_rest_auth.urls')),
    path('auth/registration', include('dj_rest_auth.registration.urls')),
]
from django.urls import path
from .views import WhoAmIView, RegisterView
from .token_views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('whoami/', WhoAmIView.as_view(), name='whoami'),
    path('register/', RegisterView.as_view(), name='register'),
]

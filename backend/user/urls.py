from django.urls import path
from .views import (
    StudentRegisterView, 
    TeacherRegisterView, 
    WhoAmIView,
    LogoutView
)
from .token_views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Registration
    path('register/student/', StudentRegisterView.as_view(), name='register-student'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='register-teacher'),

    # JWT Authentication
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Who Am I
    path('whoami/', WhoAmIView.as_view(), name='whoami'),

    #Logout
    path('logout/', LogoutView.as_view(), name='logout'),
]

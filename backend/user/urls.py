from django.urls import path
from .views import StudentRegisterView, TeacherRegisterView, WhoAmIView

urlpatterns = [
    path('register/student/', StudentRegisterView.as_view(), name='register-student'),
    path('register/teacher/', TeacherRegisterView.as_view(), name='register-teacher'),
    path('whoami/', WhoAmIView.as_view(), name='whoami'),
]

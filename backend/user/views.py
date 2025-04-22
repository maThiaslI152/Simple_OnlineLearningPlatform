from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import StudentRegisterSerializer, TeacherRegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class StudentRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [AllowAny]

class TeacherRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherRegisterSerializer
    permission_classes = [AllowAny]


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None
        }

        # Add extra data depending on the role
        if user.role == 'student':
            try:
                student_profile = user.studentprofile
                data["student_id"] = student_profile.student_id
                data["grade"] = student_profile.grade
            except StudentProfile.DoesNotExist:
                data["student_profile"] = "No student profile found."

        elif user.role == 'teacher':
            try:
                teacher_profile = user.teacherprofile
                data["expertise"] = teacher_profile.expertise
                data["department"] = teacher_profile.department
            except TeacherProfile.DoesNotExist:
                data["teacher_profile"] = "No teacher profile found."

        return Response(data)
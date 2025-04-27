# user/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentRegisterSerializer, TeacherRegisterSerializer

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'roles': {
                'is_student': user.role == 'student',
                'is_teacher': user.role == 'teacher',
                'is_admin': user.is_staff,
            }
        })


class RegisterView(APIView):
    """
    POST /api/auth/register/
    If `is_teacher` is truthy, uses TeacherRegisterSerializer;
    otherwise uses StudentRegisterSerializer.
    """
    permission_classes = []  # allow anyone

    def post(self, request):
        is_teacher = request.data.get('is_teacher') in (True, 'true', 'True', '1')
        if is_teacher:
            serializer = TeacherRegisterSerializer(data=request.data)
        else:
            serializer = StudentRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            status=status.HTTP_201_CREATED
        )

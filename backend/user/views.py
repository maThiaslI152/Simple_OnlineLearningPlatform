from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id':       user.id,
            'username': user.username,
            'email':    user.email,
            'roles': {
                'is_student': user.role == 'student',
                'is_teacher': user.role == 'teacher',
                'is_admin':   user.is_staff,
            }
        })

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Week, Note, Video, Homework, Test
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    NoteSerializer,
    VideoSerializer,
    HomeworkSerializer,
    TestSerializer
)

class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'mine']:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'students']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        return Course.objects.all()

    @action(detail=False, methods=['get'], url_path='mine')
    def mine(self, request):
        qs = self.get_queryset()
        serializer = CourseSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add_week')
    def add_week(self, request, pk=None):
        course = self.get_object()
        existing = course.weeks.values_list('week_number', flat=True)
        next_week = max(existing, default=0) + 1
        if course.weeks.filter(week_number=next_week).exists():
            return Response(
                {'error': 'Week already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Week.objects.create(course=course, week_number=next_week)
        return Response({'week_number': next_week}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        course = self.get_object()
        serializer = CourseDetailSerializer(course, context={'request': request})
        return Response(serializer.data)

class BaseModuleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'week_number']

class NoteViewSet(BaseModuleViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class VideoViewSet(BaseModuleViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class HomeworkViewSet(BaseModuleViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class TestViewSet(BaseModuleViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
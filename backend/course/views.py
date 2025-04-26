from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Week, Course, Note, Video, Homework, Test
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    NoteSerializer,
    VideoSerializer,
    HomeworkSerializer,
    TestSerializer,
)


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Allow any authenticated user to list/retrieve courses.
    Only teachers can create/update/delete or add weeks.
    """
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'mine']:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'students']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'mine']:
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        # students see only enrolled courses
        return Course.objects.filter(students=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['get'], url_path='mine')
    def mine(self, request):
        """List courses for the logged-in teacher"""
        qs = self.get_queryset()
        serializer = CourseSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add_week')
    def add_week(self, request, pk=None):
        """Create the next week for this course"""
        course = self.get_object()
        existing = course.weeks.values_list('week_number', flat=True)
        next_week = max(existing, default=0) + 1
        if course.weeks.filter(week_number=next_week).exists():
            return Response(
                {'error': f'Week {next_week} already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Week.objects.create(course=course, week_number=next_week)
        return Response({'week_number': next_week}, status=status.HTTP_201_CREATED)


class BaseModuleViewSet(viewsets.ModelViewSet):
    """
    Base for Note/Video/Homework/Test under a Course.
    Handles filtering on GET and sets course & week on save.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]
    filter_backends    = [DjangoFilterBackend]
    queryset           = None      # must be set on subclasses
    serializer_class   = None      # must be set on subclasses

    def get_queryset(self):
        course_pk   = self.kwargs.get('course_pk')
        week_number = self.request.query_params.get('week_number')
        qs = self.queryset
        if course_pk is not None:
            qs = qs.filter(course_id=course_pk)
        if week_number is not None:
            week = Week.objects.get(course_id=course_pk, week_number=week_number)
            qs = qs.filter(week=week)
        return qs

    def perform_create(self, serializer):
        course_pk   = self.kwargs.get('course_pk')
        # week_number should come from request.data
        week_number = self.request.data.get('week_number')
        week        = Week.objects.get(course_id=course_pk, week_number=week_number)
        # save with injected foreign keys
        serializer.save(course_id=course_pk, week=week)


# Subclasses declare only queryset & serializer
class NoteViewSet(BaseModuleViewSet):
    queryset         = Note.objects.all()
    serializer_class = NoteSerializer

class VideoViewSet(BaseModuleViewSet):
    queryset         = Video.objects.all()
    serializer_class = VideoSerializer

class HomeworkViewSet(BaseModuleViewSet):
    queryset         = Homework.objects.all()
    serializer_class = HomeworkSerializer

class TestViewSet(BaseModuleViewSet):
    queryset         = Test.objects.all()
    serializer_class = TestSerializer
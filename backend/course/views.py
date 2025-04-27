from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import Week, Course, Note, Video, Homework, Test, Submission
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    NoteSerializer,
    VideoSerializer,
    HomeworkSerializer,
    TestSerializer,
    SubmissionSerializer,
    WeekSerializer,
)

# -----------------------------------------------------------------------------
# Permissions
# -----------------------------------------------------------------------------
class IsTeacherOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'mine']:
            return request.user.is_authenticated
        return (
            request.user.is_authenticated and
            request.user.role == 'teacher'
        )


# -----------------------------------------------------------------------------
# Course ViewSet
# -----------------------------------------------------------------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset         = Course.objects.all()
    permission_classes = [IsTeacherOrReadOnly]
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['teacher', 'students']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'mine']:
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        return Course.objects.filter(students=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=False, methods=['get'], url_path='mine')
    def mine(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add_week')
    def add_week(self, request, pk=None):
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


# -----------------------------------------------------------------------------
# BaseModuleViewSet: all Note/Video/Homework/Test inherit from this
# -----------------------------------------------------------------------------
class BaseModuleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]
    filter_backends    = [DjangoFilterBackend]
    queryset           = None  # must be set in subclass
    serializer_class   = None  # must be set in subclass

    def get_queryset(self):
        course_pk   = self.kwargs['course_pk']
        week_number = self.kwargs.get('week_pk')  # from URL /weeks/{week_pk}/...
        qs = self.queryset.filter(course_id=course_pk)
        if week_number is not None:
            # filter modules by the Week.week_number
            qs = qs.filter(week__week_number=week_number)
        return qs

    def perform_create(self, serializer):
        course_pk   = self.kwargs['course_pk']
        week_number = self.kwargs.get('week_pk')
        # ensure the Week instance exists
        try:
            week = Week.objects.get(course_id=course_pk, week_number=week_number)
        except Week.DoesNotExist:
            raise serializers.ValidationError({
                'week_pk': f'Week {week_number} not found for course {course_pk}.'
            })
        serializer.save(
            course_id=course_pk,
            week=week
        )

# -----------------------------------------------------------------------------
# Week ViewSet (to list/add weeks under a course)
# -----------------------------------------------------------------------------
class WeekViewSet(viewsets.ModelViewSet):
    serializer_class   = WeekSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        return Week.objects.filter(course_id=course_pk)

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])

# -----------------------------------------------------------------------------
# Module ViewSets
# -----------------------------------------------------------------------------
class NoteViewSet(BaseModuleViewSet):
    queryset         = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, course_pk=None, week_pk=None, pk=None):
        note = self.get_object()
        if not note.file:
            raise Http404
        fh = note.file.open('rb')
        filename = note.file.name.rsplit('/', 1)[-1]
        return FileResponse(fh, as_attachment=False, filename=filename)

class VideoViewSet(BaseModuleViewSet):
    queryset         = Video.objects.all()
    serializer_class = VideoSerializer

class HomeworkViewSet(BaseModuleViewSet):
    queryset         = Homework.objects.all()
    serializer_class = HomeworkSerializer

    @action(
        detail=True,
        methods=['post'],
        url_path='submit',
        parser_classes=[MultiPartParser, FormParser]
    )
    def submit(self, request, course_pk=None, week_pk=None, pk=None):
        homework = self.get_object()
        if 'file' not in request.FILES:
            return Response({'error':'No file uploaded.'}, status=400)
        submission = Submission.objects.create(
            homework=homework,
            student=request.user,
            file=request.FILES['file']
        )
        return Response(SubmissionSerializer(submission).data, status=201)

class TestViewSet(BaseModuleViewSet):
    queryset         = Test.objects.all()
    serializer_class = TestSerializer
    
class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_pk   = self.kwargs.get('course_pk')
        homework_pk = self.kwargs.get('homework_pk')
        return Submission.objects.filter(
            homework_id=homework_pk,
            homework__course_id=course_pk
        )
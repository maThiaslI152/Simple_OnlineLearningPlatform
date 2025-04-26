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
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True, context={'request': request})
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
        print("STORAGE BACKEND IN NoteViewSet:", default_storage.__class__)
        # DEBUG: what files came in?
        print("DEBUG request.FILES:", self.request.FILES)

        course_pk   = self.kwargs['course_pk']
        week_number = self.request.data.get('week_number')
        week        = Week.objects.get(course_id=course_pk, week_number=week_number)

        instance = serializer.save(course_id=course_pk, week=week)
        # DEBUG: after save, what did instance.file.name become?
        print("DEBUG saved file name:", instance.file.name)


# Subclasses declare only queryset & serializer
class NoteViewSet(BaseModuleViewSet):
    queryset         = Note.objects.all()
    serializer_class = NoteSerializer

class VideoViewSet(BaseModuleViewSet):
    queryset         = Video.objects.all()
    serializer_class = VideoSerializer


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        week_number = self.request.query_params.get('week_number')

        if not week_number:
            raise serializers.ValidationError({'week_number': 'This field is required as query parameter (?week_number=).'})

        try:
            week = Week.objects.get(course_id=course_pk, week_number=week_number)
        except Week.DoesNotExist:
            raise serializers.ValidationError({'week_number': f'Week {week_number} not found for course {course_pk}.'})

        serializer.save(course_id=course_pk, week=week)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TestViewSet(BaseModuleViewSet):
    queryset         = Test.objects.all()
    serializer_class = TestSerializer

class NoteDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, course_pk, pk, format=None):
        try:
            note = Note.objects.get(pk=pk, course_id=course_pk)
        except Note.DoesNotExist:
            raise Http404

        if not note.file:
            raise Http404

        fh = note.file.open('rb')
        filename = note.file.name.rsplit('/', 1)[-1]
        return FileResponse(fh, as_attachment=False, filename=filename)
    
class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Optional: add IsTeacher permission if needed

    def get_queryset(self):
        course_pk = self.kwargs.get('course_pk')
        homework_pk = self.kwargs.get('homework_pk')
        return Submission.objects.filter(
            homework_id=homework_pk,
            homework__course_id=course_pk
        )

class HomeworkSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_pk, homework_pk):
        homework = Homework.objects.filter(id=homework_pk, course_id=course_pk).first()
        if not homework:
            return Response({'error': 'Homework not found.'}, status=status.HTTP_404_NOT_FOUND)

        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(
            homework=homework,
            student=request.user,
            file=request.FILES['file']
        )
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
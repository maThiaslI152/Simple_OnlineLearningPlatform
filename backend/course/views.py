from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.shortcuts import get_object_or_404
from .models import Course, Note, Video, Homework, Test, Week
from .serializers import (
    CourseSerializer, 
    CourseDetailSerializer, 
    NoteSerializer, 
    VideoSerializer, 
    HomeworkSerializer, 
    TestSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return CourseSerializer
        return CourseDetailSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    # ✅ Add week endpoint
    @action(detail=True, methods=['post'], url_path='add_week')
    def add_week(self, request, pk=None):
        course = self.get_object()

        existing_weeks = course.weeks.values_list('week_number', flat=True)
        next_week = max(existing_weeks, default=0) + 1

        # Check if this week already exists (safety, but not really needed with correct logic)
        if Week.objects.filter(course=course, week_number=next_week).exists():
            return Response(
                {"error": f"Week {next_week} already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Week.objects.create(course=course, week_number=next_week)
        return Response({"next_week": next_week}, status=status.HTTP_201_CREATED)

    # ✅ Custom retrieve to include weeks
    def retrieve(self, request, pk=None):
        course = self.get_object()
        available_weeks = sorted(course.weeks.values_list('week_number', flat=True))

        return Response({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "available_weeks": available_weeks,
        })

# ✅ Shared logic to avoid repeating the same filter code
def filter_by_course_and_week(queryset, request):
    course = request.query_params.get('course')
    week = request.query_params.get('week_number')
    if course:
        queryset = queryset.filter(course=course)
    if week:
        queryset = queryset.filter(week_number=week)
    return queryset

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return filter_by_course_and_week(Note.objects.all(), self.request)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return filter_by_course_and_week(Video.objects.all(), self.request)

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return filter_by_course_and_week(Homework.objects.all(), self.request)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return filter_by_course_and_week(Test.objects.all(), self.request)

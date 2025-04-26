from rest_framework import serializers
from .models import Course, Note, Video, Homework, Test
from user.models import CustomUser

# -----------------------------------
# Module serializers (flat, all fields)
# -----------------------------------

class NoteSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'course', 'week', 'title', 'content', 'file', 'file_url', 'created_at']

    def get_file_url(self, obj):
        # obj.file.url already points to MinIO://media/...
        return obj.file.url if obj.file else None

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'course', 'week', 'title', 'url', 'created_at']

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'course', 'week', 'title', 'description', 'due_date', 'created_at']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'course', 'week', 'title', 'questions', 'attempt_limit', 'time_limit', 'created_at']


# -----------------------------------
# Course serializers
# -----------------------------------

class CourseSerializer(serializers.ModelSerializer):
    # used for list & create
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'created_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    # used for retrieve
    available_weeks = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'available_weeks']

    def get_available_weeks(self, obj):
        # returns a sorted list of week numbers
        return sorted(obj.weeks.values_list('week_number', flat=True))

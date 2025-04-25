from rest_framework import serializers
from .models import Course, Note, Video, Homework, Test
from user.models import CustomUser

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField()

    class Meta:
        model = Homework
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    attempt_limit = serializers.IntegerField()  # Added for attempt limit
    time_limit = serializers.IntegerField()     # Added for time limit (minutes)

    class Meta:
        model = Test
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'students']
        read_only_fields = ['teacher']

class CourseDetailSerializer(serializers.ModelSerializer):
    weeks = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'weeks']

    def get_weeks(self, obj):
        note_weeks = obj.notes.values_list('week_number', flat=True).distinct()
        video_weeks = obj.videos.values_list('week_number', flat=True).distinct()
        homework_weeks = obj.homeworks.values_list('week_number', flat=True).distinct()
        test_weeks = obj.tests.values_list('week_number', flat=True).distinct()
        all_weeks = sorted(set(note_weeks) | set(video_weeks) | set(homework_weeks) | set(test_weeks))
        return [
            {
                'week_number': w,
                'has_note': w in note_weeks,
                'has_video': w in video_weeks,
                'has_homework': w in homework_weeks,
                'has_test': w in test_weeks
            }
            for w in all_weeks
        ]
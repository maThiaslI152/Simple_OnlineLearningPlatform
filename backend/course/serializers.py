#course/serializer
from rest_framework import serializers
from .models import Course, Note, Video, Homework, Test, Submission, Week
from user.models import CustomUser
from django.conf import settings
from minio import Minio
from datetime import timedelta

# -----------------------------------
# User serializers
# -----------------------------------
class UserSerializer(serializers.ModelSerializer):
    # expose `profile_picture.url` as `picture` (or null if none)
    picture = serializers.SerializerMethodField()

    class Meta:
        model  = CustomUser
        fields = ['id', 'username', 'picture']

    def get_picture(self, obj):
        if obj.profile_picture:
            # if using default storage, `.url` gives the public URL
            return obj.profile_picture.url
        return None

# -----------------------------------
# Module serializers (flat, all fields)
# -----------------------------------

class NoteSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'course', 'week', 'title', 'content', 'file', 'file_url', 'created_at']
        extra_kwargs = {
            'course': {'read_only': True},
            'week':   {'read_only': True},
        }

    def get_file_url(self, obj):
        # Return a presigned URL valid for a short duration
        if not obj.file:
            return None
        # Initialize MinIO client
        endpoint = settings.AWS_S3_ENDPOINT_URL.replace('http://', '').replace('https://', '')
        client = Minio(
            endpoint=endpoint,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=settings.AWS_S3_USE_SSL
        )
        # Generate presigned GET URL
        return client.presigned_get_object(
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME,
            object_name=obj.file.name,
            expires=timedelta(minutes=15)
        )

class VideoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'course', 'week', 'title', 'file', 'file_url', 'created_at']
        extra_kwargs = {
            'course': {'read_only': True},
            'week': {'read_only': True},
        }

    def get_file_url(self, obj):
        if not obj.file:
            return None
        endpoint = settings.AWS_S3_ENDPOINT_URL.replace('http://', '').replace('https://', '')
        client = Minio(
            endpoint=endpoint,
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=settings.AWS_S3_ENDPOINT_URL.startswith('https')
        )
        return client.presigned_get_object(settings.AWS_STORAGE_BUCKET_NAME, obj.file.name, expires=timedelta(minutes=15))

file_url = serializers.SerializerMethodField()

class HomeworkSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'course', 'week', 'title', 'description', 'file', 'file_url', 'created_at']
        extra_kwargs = {
            'course': {'read_only': True},
            'week': {'read_only': True},
        }

    def get_file_url(self, obj):
        if not obj.file:
            return None
        client = Minio(
            settings.AWS_S3_ENDPOINT_URL.replace('http://', '').replace('https://', ''),
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=settings.AWS_S3_ENDPOINT_URL.startswith('https')
        )
        return client.presigned_get_object(settings.AWS_STORAGE_BUCKET_NAME, obj.file.name, expires=timedelta(minutes=15))



class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'course', 'week', 'title', 'questions', 'attempt_limit', 'time_limit', 'created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    student_name = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'homework', 'student', 'student_name', 'file', 'file_url', 'submitted_at']
        extra_kwargs = {
            'student': {'read_only': True},
            'homework': {'read_only': True},
        }

    def get_file_url(self, obj):
        if not obj.file:
            return None
        client = Minio(
            settings.AWS_S3_ENDPOINT_URL.replace('http://', '').replace('https://', ''),
            access_key=settings.AWS_ACCESS_KEY_ID,
            secret_key=settings.AWS_SECRET_ACCESS_KEY,
            secure=settings.AWS_S3_ENDPOINT_URL.startswith('https')
        )
        return client.presigned_get_object(
            settings.AWS_STORAGE_BUCKET_NAME,
            obj.file.name,
            expires=timedelta(minutes=15)
        )

# -----------------------------------
# Course serializers
# -----------------------------------

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['id', 'week_number']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    teacher         = UserSerializer(read_only=True)
    available_weeks = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'available_weeks']

    def get_available_weeks(self, obj):
        # returns a sorted list of week numbers
        return sorted(obj.weeks.values_list('week_number', flat=True))

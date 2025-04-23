from rest_framework import serializers
from .models import Course
from user.models import CustomUser

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.filter(role='student'),
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'students', 'created_at']
        read_only_fields = ['teacher', 'created_at']

#user/serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, TeacherProfile

User = get_user_model()

class StudentRegisterSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(write_only=True)
    grade = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture', 'student_id', 'grade']

    # Duplicate username check
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        grade = validated_data.pop('grade')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='student',
            profile_picture=validated_data.get('profile_picture')
        )
        StudentProfile.objects.create(user=user, student_id=student_id, grade=grade)
        return user

class TeacherRegisterSerializer(serializers.ModelSerializer):
    expertise = serializers.CharField(write_only=True, required=True)
    department = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture', 'expertise', 'department']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        expertise = validated_data.pop('expertise', None)
        department = validated_data.pop('department', None)

        if not expertise or not department:
            raise serializers.ValidationError("Expertise and Department are required for teachers.")

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='teacher',
            profile_picture=validated_data.get('profile_picture')
        )

        if not TeacherProfile.objects.filter(user=user).exists():
            TeacherProfile.objects.create(user=user, expertise=expertise, department=department)

        return user
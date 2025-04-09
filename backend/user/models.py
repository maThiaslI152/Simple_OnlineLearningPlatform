from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class UserAccount(models.Model):
    ROLE_CHOICES = (
        ('student', "Student"),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

class StudentProfile(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    enrolled_course = models.ManyToManyField('courses.Course', related_name='students')
    progress = models.JSONField(default=dict)
    test_scores = models.JSONField(default=dict)

    def __str__(self):
        return f"Student: {self.account.full_name}"

    def clean(self):
        if self.account.role != 'student':
            raise ValidationError("Only users with role 'student' can have a Student profile.")

class TeacherProfile(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    teaching_course = models.ManyToManyField('courses.Course', related_name='teachers')
    certificates = models.JSONField(default=dict)
    bio = models.TextField()

    def __str__(self):
        return f"Teacher: {self.account.full_name}"

    def clean(self):
        if self.account.role != 'teacher':
            raise ValidationError("Only users with role 'Teacher' can have a Student profile.")
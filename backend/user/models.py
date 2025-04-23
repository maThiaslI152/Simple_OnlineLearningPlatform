from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.role:
            self.role = self.role.lower()  # Enforce lowercase role
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()  # This calls the clean() before saving!
        super().save(*args, **kwargs)

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    grade = models.CharField(max_length=10)

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

from django.db import models
from user.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(CustomUser, related_name='courses', limit_choices_to={'role': 'student'}, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Week(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='weeks')
    week_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('course', 'week_number')

    def __str__(self):
        return f"Week {self.week_number} ({self.course.title})"

class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='notes')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()  # Markdown or plain text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note: {self.title} ({self.course.title})"

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')  # MinIO handles this path
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video: {self.title} ({self.course.title})"

class Homework(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='homeworks')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='homeworks', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='homeworks/')  # MinIO handles this path
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Homework: {self.title} ({self.course.title})"

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    title = models.CharField(max_length=200)
    questions = models.JSONField()  # Structured questions/answers
    created_at = models.DateTimeField(auto_now_add=True)
    attempt_limit = models.PositiveIntegerField(default=1)
    time_limit = models.PositiveIntegerField(null=True, blank=True)  # Time limit (in minutes)

    def __str__(self):
        return f"Test: {self.title} ({self.course.title})"

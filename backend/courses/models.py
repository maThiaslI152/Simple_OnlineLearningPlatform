from django.db import models

# Create your models here.
class CourseSubmission(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=20, choices=(('homework', 'Homework'), ('test', 'Test')))
    file = models.FileField(upload_to='submissions/')
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.account.full_name} - {self.submission_type} ({self.course})"

class LessonProgress(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE)
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(auto_now=True)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.account.full_name} - {self.lesson} (Completed: {self.is_completed})"

from django.db import models
from user.models import CustomUser

class Course(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    teacher     = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='taught_courses'
    )
    students    = models.ManyToManyField(
        CustomUser,
        related_name='enrolled_courses',
        limit_choices_to={'role': 'student'},
        blank=True
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Week(models.Model):
    course      = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='weeks'
    )
    week_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('course', 'week_number')
        ordering = ['week_number']

    def __str__(self):
        return f"{self.course.title} - Week {self.week_number}"

class Note(models.Model):
    course      = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    week        = models.ForeignKey(
                     Week,
                     on_delete=models.CASCADE,
                     null=True,
                     blank=True,
                     help_text="Make nullable temporarily for migrations"
                 )
    title       = models.CharField(max_length=200)
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    course      = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    week        = models.ForeignKey(
        Week,
        on_delete=models.CASCADE,
        related_name='videos',
        null=True,
        blank=True,
        help_text="Temporarily nullable for migrations"
    )
    title       = models.CharField(max_length=200)
    url         = models.URLField(
                    blank=True,
                   default='',
                   help_text="Optional: link to the video"
                )
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Homework(models.Model):
    course       = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='homeworks'
    )
    week         = models.ForeignKey(
                     Week,
                     on_delete=models.CASCADE,
                     null=True,
                     blank=True,
                     help_text="(temporarily nullable so migrations run cleanly)"
                 )
    title        = models.CharField(max_length=200)
    description  = models.TextField()
    due_date     = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Test(models.Model):
    course       = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    week         = models.ForeignKey(
        Week,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Temporarily nullable for migrations"
    )
    title        = models.CharField(max_length=200)
    questions    = models.JSONField()
    attempt_limit= models.PositiveIntegerField(default=1)
    time_limit   = models.PositiveIntegerField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
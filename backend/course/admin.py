from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('students',) 

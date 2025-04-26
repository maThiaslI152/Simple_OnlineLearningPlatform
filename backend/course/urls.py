from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import (
    CourseViewSet,
    HomeworkViewSet,
    SubmissionViewSet,
    NoteViewSet,
    VideoViewSet,
    TestViewSet,
    HomeworkSubmitView,
    NoteDownloadView
)

# Main router: register courses
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

# Nested router: homework, notes, videos, tests under course
courses_router = NestedSimpleRouter(router, r'course', lookup='course')
courses_router.register(r'homework', HomeworkViewSet, basename='course-homework')
courses_router.register(r'note', NoteViewSet, basename='course-note')
courses_router.register(r'video', VideoViewSet, basename='course-video')
courses_router.register(r'test', TestViewSet, basename='course-test')

# Nested router: submissions under homework
homework_router = NestedSimpleRouter(courses_router, r'homework', lookup='homework')
homework_router.register(r'submissions', SubmissionViewSet, basename='homework-submissions')

urlpatterns = [
    # Main and nested routers
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(homework_router.urls)),

    # Extra actions (submit homework, download note)
    path('course/<int:course_pk>/homework/<int:homework_pk>/submit/', HomeworkSubmitView.as_view(), name='homework-submit'),
    path('course/<int:course_pk>/note/<int:pk>/download/', NoteDownloadView.as_view(), name='note-download'),
]

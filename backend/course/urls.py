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
    WeekViewSet,
)

# Main router: register courses
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

 # first level nesting courses: /courses/{course_pk}/…
courses_router = NestedSimpleRouter(router, r'courses', lookup='course')

# register weeks
courses_router.register(r'weeks', WeekViewSet, basename='course-weeks')

# second level nesting week_pk: /courses/{course_pk}/weeks/{week_pk}/…
weeks_router = NestedSimpleRouter(courses_router, r'weeks', lookup='week')
weeks_router.register(r'notes',    NoteViewSet,     basename='week-notes')
weeks_router.register(r'videos',   VideoViewSet,    basename='week-videos')
weeks_router.register(r'homework', HomeworkViewSet, basename='week-homework')
weeks_router.register(r'tests',    TestViewSet,     basename='week-tests')

# third level nesting: submissions under homework
homework_router = NestedSimpleRouter(weeks_router, r'homework', lookup='homework')
homework_router.register(r'submissions', SubmissionViewSet, basename='homework-submissions')

urlpatterns = [
    # Main and nested routers
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(weeks_router.urls)),
    path('', include(homework_router.urls)),
 ]
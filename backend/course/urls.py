# course/urls.py
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import CourseViewSet, NoteViewSet, VideoViewSet, HomeworkViewSet, TestViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course') # mount at /api/course/

# Instead, point it at the empty-prefix parent
courses_router = NestedSimpleRouter(router, r'', lookup='course')

courses_router.register(r'note',     NoteViewSet,     basename='course-note')
courses_router.register(r'video',    VideoViewSet,    basename='course-video')
courses_router.register(r'homework', HomeworkViewSet, basename='course-homework')
courses_router.register(r'test',     TestViewSet,     basename='course-test')

urlpatterns = router.urls + courses_router.urls

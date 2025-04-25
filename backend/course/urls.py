from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, NoteViewSet, VideoViewSet, HomeworkViewSet, TestViewSet

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')
router.register(r'note', NoteViewSet, basename='note')
router.register(r'video', VideoViewSet, basename='video')
router.register(r'homework', HomeworkViewSet, basename='homework')
router.register(r'test', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls)),
]

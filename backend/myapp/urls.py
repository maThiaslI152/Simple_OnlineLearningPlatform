from django.urls import path
from .views import cached_data
from .views import run_task

urlpatterns = [
    path('cache/', cached_data),
    path('run-task/', run_task),
]

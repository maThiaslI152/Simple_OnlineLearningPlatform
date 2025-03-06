from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.tasks import add

@api_view(['GET'])
def cached_data(request):
    data = cache.get('my_data')
    if not data:
        data = {'message': 'Hello, World!'}  # Simulate data fetching
        cache.set('my_data', data, timeout=60)  # Cache for 60 seconds
    return Response(data)

@api_view(["GET"])
def run_task(request):
    task = add.delay(10, 20)  # Ensure two values are passed
    return Response({"task_id": task.id, "message": "Task is running!"})
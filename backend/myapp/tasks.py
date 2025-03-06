from celery import shared_task

@shared_task
def add(x, y):
    print(f"Task received arguments: x={x}, y={y}")  # Debugging
    return x + y

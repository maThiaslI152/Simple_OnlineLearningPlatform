from celery import shared_task
from django.core.cache import cache

@shared_task
def add(x, y):
    return x + y

@shared_task
def debug_task():
    print("Celery is working!")

@shared_task
def test_redis_cache():
    # Store a value in Redis cache
    cache.set("celery_test_key", "Hello from Celery & Redis!", timeout=60)

    # Retrieve the value from Redis
    cached_value = cache.get("celery_test_key")

    return f"Stored in Redis: {cached_value}"
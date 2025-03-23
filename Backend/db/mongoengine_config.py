from mongoengine import connect
from django.conf import settings

def connect_to_mongo():
    connect(
        db=settings.MONGODB_SETTINGS['db'],
        host=settings.MONGODB_SETTINGS['host'],
        port=settings.MONGODB_SETTINGS['port'],
        username=settings.MONGODB_SETTINGS.get('username'),
        password=settings.MONGODB_SETTINGS.get('password'),
        authentication_source=settings.MONGODB_SETTINGS.get('authentication_source', 'admin')
    )

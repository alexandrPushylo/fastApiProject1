from celery import Celery

from src.config import settings

celery_instance = Celery(
    'tasks',
    broker_url=settings.REDIS_URL,
    include=[
        'src.tasks.tasks',
    ],
)
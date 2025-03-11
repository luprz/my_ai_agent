import os
from celery import Celery

# Get Redis URL from environment variable
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Celery app
celery_app = Celery(
    'app',
    broker=redis_url,
    backend=redis_url,
    include=['app.events.main_assistant_event']
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

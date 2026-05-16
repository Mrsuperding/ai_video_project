"""
Celery Application Configuration
"""
from celery import Celery

from app.config import settings

# Create Celery app
celery_app = Celery(
    "ai_video_platform",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.video_tasks",
        "app.tasks.ai_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3000,  # 50 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "app.tasks.cleanup.cleanup_expired_sessions",
        "schedule": 3600.0,  # Every hour
    },
    "update-statistics": {
        "task": "app.tasks.statistics.update_platform_statistics",
        "schedule": 3600.0,  # Every hour
    },
}


@celery_app.task
def hello_world():
    """Test task"""
    return "Hello from Celery!"

"""
Celery configuration for Dental Management System
Handles background tasks like appointment reminders, email notifications, etc.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dentalmanagement.settings')

# Create Celery app
app = Celery('dentalmanagement')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule for Periodic Tasks
app.conf.beat_schedule = {
    # Send appointment reminders every hour
    'send-appointment-reminders': {
        'task': 'home.tasks.send_appointment_reminders',
        'schedule': crontab(minute=0),  # Every hour
    },
    # Clean up old sessions daily
    'cleanup-old-sessions': {
        'task': 'home.tasks.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    # Generate daily reports for doctors
    'generate-daily-reports': {
        'task': 'home.tasks.generate_daily_reports',
        'schedule': crontab(hour=8, minute=0),  # Daily at 8 AM
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')

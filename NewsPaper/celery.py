import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_message_every_weekly_new_post': {
        'task': 'news.tasks.send_message_every_weekly_new_post',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # каждые 10 сек для проверки корректности настроек
        # 'schedule': 10,
        'args': (False,),
    },
}

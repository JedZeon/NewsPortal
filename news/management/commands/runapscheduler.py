import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, UserCategory, User
from django.utils.timezone import make_aware

from news.functions import send_message_html
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    # make_aware(value, timezone=None)[исходный код]
    # Возвращает осознанный datetime, который представляет тот же момент времени, что и value в timezone, value
    # являющийся наивным datetime.Если timezone задано None, то по умолчанию возвращается current time zone.

    # Получаем все посты за прошедшую неделю
    week_start = make_aware(datetime.now() - timedelta(days=7))
    posts = Post.objects.filter(date_time__gte=week_start)
    # print(posts.count())
    if posts.count() > 0:
        # Список категорий в которых были новости
        categories_ = set(posts.values_list('categories__name', flat=True))
        # Все подписанные юзвери в этих категориях
        sub_users = set(
            UserCategory.objects.filter(category__name__in=categories_).values_list('user', flat=True))
        for sub_user in sub_users:
            cat_users = set(UserCategory.objects.filter(user=sub_user).values_list('category__name', flat=True))
            posts_user = posts.filter(categories__name__in=cat_users)

            user_ = User.objects.get(id=sub_user)
            if user_.email:
                html_context = render_to_string(
                    'message_week_post.html',
                    {
                        'posts_user': posts_user,
                        'user_': user_,
                        'SITE_URL': settings.SITE_URL,
                        'cat_users': cat_users
                    }
                )

                # print(html_context)
                send_message_html(to=[user_.email], subject='Новые статьи за неделю.', html_message=html_context)
            print('Отправлено')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # Каждый понедельник в 00:00
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            # каждые 5 секунд
            # trigger=CronTrigger(second="*/5"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

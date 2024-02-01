from django.template.loader import render_to_string
from NewsPaper import settings
from celery import shared_task
from .functions import send_message_html, send_message_weekly

# import time

from news.models import Post, UserCategory


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")

@shared_task
def send_email_subscribers(pk):
    post = Post.objects.get(pk=pk)
    cat_user = UserCategory.objects.filter(category__in=post.categories.all())

    for cat in cat_user:
        # Проверка есть ли емайл
        if not cat.user.email:
            continue

        # формируем html сообщения
        html_content = render_to_string(
            'message.html', {
                'post': post,
                'username': cat.user,
                'link': f'{settings.SITE_URL}/news/{post.pk}'
            }
        )
        send_message_html(to=[cat.user.email], subject=post.title, html_message=html_content)


@shared_task
def send_message_every_weekly_new_post(test=False):
    # print('******************** test hello!!! ********************', test)
    send_message_weekly(test=test)

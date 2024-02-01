from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from news.models import Post, UserCategory, User
from django.utils.timezone import make_aware
from datetime import datetime, timedelta


def send_message_html(to, subject='', message='', html_message='', test=False):
    if not test:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=to
        )
        msg.attach_alternative(html_message, "text/html")  # добавляем html
        msg.send()  # отсылаем
    else:
        print(f'Отправка для: {to} - {subject}')


def send_message_weekly(test=False):
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
                send_message_html(
                    to=[user_.email],
                    subject='Новые статьи за неделю.',
                    html_message=html_context,
                    test=test
                )
                print('Отправлено')

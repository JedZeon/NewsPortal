from django.template.loader import render_to_string

from NewsPaper import settings
from .models import Post, UserCategory

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .functions import send_message_html

from .tasks import send_email_subscribers


# from allauth.account.signals import email_confirmed


# Олег Афанасьев | ментор
# Здравствуйте!
# Из-за связи многие ко многим между постами и категориями, мы не можем при создании поста сразу назначить ему одну или
# несколько категорий. Эта связь реализуется через идентификаторы поста и категории в промежуточной таблице.
# Поэтому нужно предварительно создать пост, чтобы для него был сформирован идентификатор, по которому в дальнейшем
# можно будет уже связать пост с категорией.
# Поэтому при срабатывании сигнала post_save у поста еще не будет связанных категорий и ваше уведомление никому не
# отправится.
# В данном случае нужно использовать сигнал m2m_changed


@receiver(signal=m2m_changed, sender=Post.categories.through)
def post_save_m2m_changed(instance, action, **kwargs):
    if action == 'post_add':
        variant = 3

        if variant == 3:
            # Создание задачи на отправку писем для подписанных на категории
            send_email_subscribers.delay(instance.pk)

        if variant == 2:
            # Отправка писем уведомлений о новой новости в категории
            cat_user = UserCategory.objects.filter(category__in=instance.categories.all())

            for cat in cat_user:
                # Проверка есть ли емайл
                if cat.user.email:
                    # формируем html сообщения
                    html_content = render_to_string(
                        'message.html', {
                            'post': instance,
                            'username': cat.user,
                            'link': f'{settings.SITE_URL}/news/{instance.pk}'
                        }
                    )
                    send_message_html(to=[cat.user.email], subject=instance.title, html_message=html_content)

        if variant == 1:
            # Перебираем все категории поста
            for post_category in instance.categories.all():
                # перебираем пользователей подписанных на категорию
                mail_user_send = []
                for p_category in UserCategory.objects.filter(category=post_category):
                    if p_category.user.email:
                        # Чтобы не дублировать отправку запомним кому отправили
                        if not (p_category.user.email in mail_user_send):
                            mail_user_send.append(p_category.user.email)

                            # формируем html сообщения
                            html_content = render_to_string(
                                'message.html', {
                                    'post': instance,
                                    'username': p_category.user,
                                    'link': f'{settings.SITE_URL}/news/{instance.pk}'
                                }
                            )

                            send_message_html(to=[p_category.user.email], subject=instance.title,
                                              html_message=html_content)

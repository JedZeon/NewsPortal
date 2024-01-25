from django.core.mail import mail_managers, send_mail
from .models import Post, Category, UserCategory

from django.db.models.signals import post_save
from django.dispatch import receiver


# sender - от кого будит приходить сигнал
# instance - данные записи
# created - есть ли уже в базе (создание / редактирование)
@receiver(post_save, sender=Post)
def notify_user(sender, instance, created, **kwargs):
    if created:
        print(f'НОВОЕ - {instance}: {instance.date_time.strftime("%d/%m/%Y")}')
        for post_category in instance.categories.all():
            mail_user_send = []
            print(post_category)
            for category in UserCategory.objects.filter(category=post_category):
                print(f'юзверь - {category.user}, категория {category.category}')
                if category.user.email:
                    mail_user_send.append(category.user.email)

            print(mail_user_send)
            if mail_user_send:
                pass
        # отправляем письмо
        # send_mail(
        #     subject=f'{instance.date_time.strftime("%Y-%M-%d")}: {instance.title}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=instance.preview(),  # сообщение с кратким описанием проблемы
        #     from_email='jedcrb@mail.ru',
        #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=mail_user_send,
        #     # здесь список получателей. Например, секретарь, сам врач и т. д.
        #     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! для тестового сервера
        #     fail_silently=True
        # )

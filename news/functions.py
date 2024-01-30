from django.core.mail import mail_managers, send_mail, EmailMultiAlternatives
from django.conf import settings


def send_message_html(to, subject='', message='', html_message=''):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=to
    )
    msg.attach_alternative(html_message, "text/html")  # добавляем html
    msg.send()  # отсылаем

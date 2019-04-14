from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_confirm(to: str, url_email_confirm: str):
    """
    Отправка ссылки для подтверждения емейл адреса

    :param to: Адрес электронной почты получателя
    :param url_email_confirm: url, который будет отправлен на почту, для ее подтверждения
    """

    context_data = {
        'url_email_confirm': url_email_confirm,
        'confirm_text': 'Подтвердить электронную почту'
    }

    body_message = render_to_string('email/send_confirm_email.html', context_data)

    subject = 'Подтверждение email'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to]

    msg = EmailMultiAlternatives(subject, body_message, from_email, recipient_list)
    msg.attach_alternative(body_message, 'text/html')
    return msg.send()

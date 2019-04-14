import logging
from blog_backend.celery import app
from blog_backend.notifications.email.send import send_email_confirm


@app.task()
def user_send_activation_email(email, url_email_confirm):
    if send_email_confirm(email, url_email_confirm) == 1:
        logging.warning(f'SUCCESS: сообщение успешно отправлено: {email}')
    else:
        logging.warning(f'ERROR: сообщение не отправлено: {email}')

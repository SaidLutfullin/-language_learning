from django.core.mail import send_mail
from django.conf import settings
from loguru import logger

def send_email(user_id, form_data):

    send_mail(subject='Сообщение через форму обратной связи на сайте',
            message= 'От {0}, e-mail: {1}. \n{2}'.format(form_data['name'], form_data['email'], form_data['message']),
            from_email=None,
            recipient_list=[settings.DEFAULT_FROM_EMAIL, ])

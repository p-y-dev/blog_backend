import os
import urllib.parse as urlparse
import uuid
from datetime import timedelta

from django.utils import timezone


def forming_url_with_params(url: str, params: dict) -> str:
    """
    Формирование url с GET параметрами

    :param url: url
    :param params: параметры для формирования url
    :return: url с GET параметрами
    """

    url_parts = list(urlparse.urlparse(url))
    url_parts[4] = urlparse.urlencode(params)
    return urlparse.urlunparse(url_parts)


def life_time_is_correct(life_time_seconds: int, created_at: timezone) -> bool:
    """
    Проверка на то, действителен ли объект в системе с момента его создания

    :param life_time_seconds: Время жизни объекта в секундах
    :param created_at: Дата и время создания объекта в системе
    :return: Flase - время жизни объекта закончилось, иначе True
    """

    current_date_time = timezone.now()
    time_delta = timedelta(seconds=life_time_seconds)

    if current_date_time > created_at + time_delta:
        return False

    return True


def generate_token(val) -> str:
    """
    Создание уникального токена

    :param val: Значение, которое будет участвовать в случайной генерации
    :return: Возвращает случайный токен
    """

    return str(uuid.UUID(bytes=os.urandom(16), version=4)) + str(val)

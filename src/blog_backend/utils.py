import urllib.parse as urlparse


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

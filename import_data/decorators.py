from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .logger.logger import logger
from . import redis

import functools


def create_log_info(func):
    """Декоратор выполняющий логирование со статусом INFO"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info('created {}'.format(result))
        return result
    return wrapper


def check_status_import_data(func):
    """Декоратор выполняющий обращение к redis, проверяет в redis статус импорта"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        status = redis.connection.get('import_data')
        status = status if status is None else bool(int(status.decode('utf-8')))
        request = args[1]
        tag, message = redis.STATUS_IMPORT_DATA.get(status).values()
        messages.add_message(request, tag, message)
        result = func(*args, **kwargs)
        return result
    return wrapper


def loading_status(func):
    """Декоратор выполняющий обращение к redis, записывает в redis статус импорта"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        redis.connection.set('import_data', 1)
        try:
            result = func(*args, **kwargs)
            redis.connection.delete('import_data')
            return result
        except ObjectDoesNotExist as err:
            logger.error('{}'.format(err))
            redis.connection.set('import_data', 0)
            return None

    return wrapper

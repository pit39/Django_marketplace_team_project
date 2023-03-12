"""Создние объекта подключения к redis"""

from django.contrib import messages
from django.utils.translation import gettext_lazy as _

import redis


connection = redis.Redis(host='redis', port=6379, db=0)


STATUS_IMPORT_DATA = {
    True: {
        'tag': messages.ERROR,
        'message': _('Идет импорт'),
    },
    False: {
        'tag': messages.ERROR,
        'message': _('Импорт не выполнен'),
    },
    None: {
        'tag': messages.INFO,
        'message': _('Вы можете импортровать данные'),
    },
}

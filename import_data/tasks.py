"""Логика асинхронной загрузки дынных из файла в базу данных"""

from config.celery import app
from typing import Union

from django.db.models import Model

from .tools import load_object
from .data_validators import ProductShopData, Product, Shop
from .decorators import loading_status

import importlib


@app.task
@loading_status
def import_data_to_db(data: str, user_email) -> None:
    data = ProductShopData.parse_raw(data)
    for object_name in data.objects:
        model_name: str = object_name[:-1].title()
        for object_i in data.objects[object_name]:
            object_: Union[Product, Shop] = data.objects[object_name][object_i]

            model_class: Model = getattr(
                importlib.import_module('{}.models'.format(model_name.lower())), '{}'.format(model_name)
            )
            load_object(model_name)(object_, model_class, user_email)

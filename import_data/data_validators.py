"""Модели из модуля pydantic для валидации импортируемых json данных"""

from django.utils.translation import gettext_lazy as _

from pydantic import BaseModel, validator
from typing import Dict, Union

import re


class Property(BaseModel):
    name: str


class ProductProperty(BaseModel):
    property: Property
    value: str


class Product(BaseModel):
    name: str
    category: str
    description: str
    properties: list[ProductProperty]


class Shop(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    description: str
    slug: str

    @validator('phone')
    def phone_validator(cls, v: str):
        result = re.match(r'\+\d{,15}', v)
        if not result or not v[1:].isdigit():
            raise ValueError(_('Введите валидный номер телефона'))
        return v


class ProductShopData(BaseModel):
    objects: Dict[str, Dict[str, Union[Product, Shop]]]

"""Логика создания каждого объекта в базе данных"""

from django.db.models import Model
from django.db.utils import IntegrityError

from product.models import ProductProperty, Property
from category.models import Category
from users.models import CustomUser

from . import decorators
from . import data_validators


@decorators.create_log_info
def load_product(data_object: data_validators.Product, model_class: Model, *args):
    """Создание объекта модели продукта в БД"""
    category, _ = Category.objects.get_or_create(name=data_object.category)
    product, _ = model_class.objects.get_or_create(name=data_object.name,
                                                   category=category,
                                                   description=data_object.description)
    for property_ in data_object.properties:
        ProductProperty.objects.get_or_create(
            product=product,
            property=Property.objects.get_or_create(name=property_.property.name)[0],
            value=property_.value
        )
    return product


@decorators.create_log_info
def load_shop(data_object: data_validators.Shop, models_class: Model, user_email: str):
    """Создание объекта модели магазина в БД"""
    holder = CustomUser.objects.get(email=user_email)
    try:
        shop = models_class.objects.create(logo=None, holder=holder, **data_object.dict())
    except IntegrityError:
        shop = models_class.objects.get(**data_object.dict())
    return shop


def load_object(model_name):
    """Функция возращает объект другой функции в звисимости от имени модели на входе в функцию"""
    dict_methods: dict = {
        'Product': load_product,
        'Shop': load_shop,
    }
    return dict_methods.get(model_name)

from typing import Optional

from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

from users.models import CustomUser
from cart.models import ProductInCart


def register_user(request, user_form) -> None:
    """Функция, создает пользователя и авторизует его"""
    user_form.save()

    anonim_cart = get_cart_from_anonim(request)
    email = user_form.cleaned_data.get('email')
    raw_password = user_form.cleaned_data.get('password1')

    user = authenticate(email=email, password=raw_password)

    if anonim_cart and user:
        move_cart_from_session(anonim_cart, user)
        del request.session['cart']

    group = Group.objects.get(name='customer')
    user.groups.add(group)

    login(request, user)


def login_user(request, form) -> CustomUser:
    """Функция, авторизует пользователя"""
    anonim_cart = get_cart_from_anonim(request)
    user = form.cleaned_data
    login(request, user)

    if anonim_cart and user:
        move_cart_from_session(anonim_cart, user)
        del request.session['cart']


def password_change(request, user_form) -> None:
    """Функция заглушка для представления восстановления пароля"""
    email = user_form.cleaned_data.get('email')
    user = CustomUser.objects.get(email=email)
    user.set_password('qwerty1234')
    user.save()


def get_cart_from_anonim(request) -> Optional[dict]:
    """Функция, возвращает корзину не авторизованного пользователя"""
    cart = request.session.get('cart')
    if cart:
        data = {}
        for key, values in cart.items():
            data[key] = {
                'shop_product_id': values['shop_product_id'],
                'quantity': values['quantity'],
                'price': values['price'],
            }

        return data


def move_cart_from_session(cart: dict, user: CustomUser) -> None:
    """
    Функция, преобразует корзину неавторизованного пользователя в корзину авторизованного,
    если у пользователя уже были такие товары в корзине, суммирует количество
    """
    for product_id, data in cart.items():
        obj, created = ProductInCart.objects.get_or_create(
            user=user,
            shop_product__product_id=product_id,
            defaults={
                'shop_product_id': data['shop_product_id'],
            })

        obj.shop_product_id = data['shop_product_id']
        obj.quantity += data['quantity']
        obj.save()

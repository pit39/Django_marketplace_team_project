def check_cart_number(card_number: int) -> bool:
    """Функция проверяет возможность оплаты с карты"""
    if len(str(card_number)) != 8 or not isinstance(card_number, int) or card_number % 2 \
            or str(card_number)[-1] == '0':
        return False

    return True

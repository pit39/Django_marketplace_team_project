from .models import ViewsHistory


class PersonalAccount:

    @staticmethod
    def add_viewed_product(user, product):
        """ Добавление продукта в список просмотренных """
        try:
            history_object = ViewsHistory.objects.get(user_id=user, product_id=product)
            history_object.delete()
            ViewsHistory.objects.create(user_id=user, product_id=product)
        except ViewsHistory.DoesNotExist:
            ViewsHistory.objects.create(user_id=user, product_id=product)

    @staticmethod
    def delete_viewed_product(user, product):
        """ Удаление продукта из списка просмотренных """
        history_object = ViewsHistory.objects.get(user_id=user, product_id=product)
        history_object.delete()

    @staticmethod
    def get_last_viewed(user):
        """ Получение списка просмотренных продуктов """
        history_objects = ViewsHistory.objects.filter(user_id=user).all()
        return history_objects

    @staticmethod
    def is_viewed(user, product):
        """ Узнать, есть ли товар в списке просмотренных """
        try:
            ViewsHistory.objects.get(user_id=user, product_id=product)
            return True
        except ViewsHistory.DoesNotExist:
            return False

    @staticmethod
    def get_count_viewed(user):
        """ Получение количества просмотренных продуктов """
        history_objects = ViewsHistory.objects.filter(user=user).count()
        return history_objects

    def get_profile_data(self):
        """ Получение данных профиля """
        pass

    def set_profile_data(self):
        """ Внесение изменений в профиль """
        pass

    def get_order_history(self):
        """ Получение истории заказов """
        pass

    def get_order_data(self):
        """ Получение данных конкретного заказа """
        pass

    def registration(self):
        """ Регистрация """
        pass

    def authorization(self):
        """ Авторизация """
        pass

    def logout(self):
        """ Логаут """
        pass

    def restore_password(self):
        """ Восстановление пароля """
        pass

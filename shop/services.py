from product.models import Product
from users.models import CustomUser
from .models import Shop


class ShopServices:
    @classmethod
    def get_all_shops(cls):
        shops = Shop.objects.all()
        return shops

    @classmethod
    def get_all_goods(cls):
        goods = Product.objects.all()
        return goods

    @classmethod
    def get_user_shop(cls, user: CustomUser):
        shops = Shop.objects.all().filter(holder=user)
        return shops

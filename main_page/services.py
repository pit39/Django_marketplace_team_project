from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from catalog.models import Favourite, DayOffer, Limit
from discount.models import ProductDiscount
from discount.services import get_discounts_queryset
from product.models import Product
from .models import Banner
from django.conf import settings
import random
from django.utils import timezone

BANNERS_LEN = settings.BANNERS_LEN
FAVOURITE_CAT_LEN = settings.FAVOURITE_CAT_LEN
TOP_PRODUCTS_LEN = settings.TOP_PRODUCTS_LEN
HOT_OFFERS_LEN = settings.HOT_OFFERS_LEN
LIMITED_OFFERS_LEN = settings.LIMITED_OFFERS_LEN


class MainPage:

    @staticmethod
    def get_banners():
        """ получение баннеров """
        banner = Banner.objects.all()
        if banner:
            banner_list = list(banner)
            if len(banner_list) > BANNERS_LEN:
                banners = random.sample(banner_list, BANNERS_LEN)
            else:
                banners = banner_list
        else:
            banners = None
        return banners

    @staticmethod
    def get_favourite_categories():
        """ получение избранных категорий """
        favourite_categories_queryset = Favourite.objects.all()
        if favourite_categories_queryset:
            favourite_categories_list = list(favourite_categories_queryset)
            if len(favourite_categories_list) > FAVOURITE_CAT_LEN:
                favourite_categories = random.sample(favourite_categories_list, FAVOURITE_CAT_LEN)
            else:
                favourite_categories = favourite_categories_list
        else:
            favourite_categories = None
        return favourite_categories

    @staticmethod
    def get_day_offer():
        """ получение предложения дня """
        try:
            day_offer = DayOffer.objects.get(day=timezone.now().date())
        except ObjectDoesNotExist:
            day_offer = None
        return day_offer

    @staticmethod
    def get_top_products():
        """ получение топ-товаров """
        top_products = Product.objects.all().annotate(sold_amount=Coalesce(Sum('shop_products__amount'), 0))
        top_products = top_products.order_by('-sort_index', '-sold_amount')[:TOP_PRODUCTS_LEN]
        return top_products

    @staticmethod
    def get_hot_offers():
        """ получение горячих предложений """
        active_discounts = get_discounts_queryset(ProductDiscount)
        hot_offers_queryset = Product.objects.filter(
            Q(discounts__discount__in=active_discounts) | Q(category__discounts__discount__in=active_discounts))
        if len(hot_offers_queryset) <= HOT_OFFERS_LEN:
            hot_offers = hot_offers_queryset
        else:
            hot_offers_list = list(hot_offers_queryset)
            hot_offers = random.sample(hot_offers_list, HOT_OFFERS_LEN)
        return hot_offers

    @classmethod
    def get_limited_offers(cls):
        """ получение ограниченного тиража """
        day_offer = cls.get_day_offer()
        if day_offer:
            limited_offers = Limit.objects.exclude(product=day_offer.product)[:LIMITED_OFFERS_LEN]
        else:
            limited_offers = Limit.objects.all()[:LIMITED_OFFERS_LEN]
        return limited_offers

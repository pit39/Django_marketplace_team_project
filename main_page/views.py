from django.shortcuts import render
from django.views import View
from administration.models import Cache
from .services import MainPage


class MainPageView(View):

    def get(self, request):
        banners = MainPage.get_banners()
        hot_offers = MainPage.get_hot_offers()
        top_products = MainPage.get_top_products()
        favourite_categories = MainPage.get_favourite_categories()
        day_offer = MainPage.get_day_offer()
        limited_offers = MainPage.get_limited_offers()
        try:
            main_cache = Cache.objects.get(name='Main cache')
        except Cache.DoesNotExist:
            main_cache = None
        context = {
            'banners': banners,
            'favourite_categories': favourite_categories,
            'day_offer': day_offer,
            'top_products': top_products,
            'hot_offers': hot_offers,
            'limited_offers': limited_offers,
            'main_cache': main_cache.value if main_cache is not None else main_cache,
        }
        return render(request, 'main_page/main_page.html', context)


class ContactsView(View):
    def get(self, request):
        return render(request, 'main_page/contacts.html')

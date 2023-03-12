from celery import shared_task
from random import choice
from catalog.models import DayOffer, Limit
from django.utils import timezone


@shared_task
def day_offer_update():
    today = timezone.now().date()
    past_week = today - timezone.timedelta(days=7)
    old_day_offers = DayOffer.objects.filter(day__lt=past_week)
    old_day_offers.delete()
    day_offer = DayOffer.objects.filter(day=today).exists()
    limited_offers = Limit.objects.all()
    if not day_offer and limited_offers:
        limited_offer = choice(limited_offers)
        DayOffer.objects.create(day=timezone.now().date(), product=limited_offer.product)

from django.contrib import admin
from . import models


@admin.register(models.Favourite)
class FavouriteModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DayOffer)
class DayOfferModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Hot)
class HotModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Limit)
class LimitModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Top)
class TopModelAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin

from . import models


@admin.register(models.Shop)
class ShopModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    pass

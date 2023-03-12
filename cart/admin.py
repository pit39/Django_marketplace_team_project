from django.contrib import admin

from .models import ProductInCart


@admin.register(ProductInCart)
class ProductInCartAdmin(admin.ModelAdmin):
    pass

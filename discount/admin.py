from django.contrib import admin
from .models import DiscountedProduct, DiscountedCategory, DiscountedPackCategory, \
    DiscountedPackProduct, ProductDiscount, PackDiscount, CartDiscount
from django.template.defaultfilters import truncatechars
from .services import check_valid_pack_discount
from django.utils.translation import gettext_lazy as _


class BaseDiscountAdmin(admin.ModelAdmin):

    exclude = ['id']
    list_display = ['id', 'title', 'short_descr', 'active', 'type', 'value', 'priority']
    list_display_links = ['id', 'title']

    def short_descr(self, obj):
        return truncatechars(obj.description, 15)


class BaseInline(admin.TabularInline):
    extra = 0


class ProductInline(BaseInline):
    model = DiscountedProduct


class CategoryInline(BaseInline):
    model = DiscountedCategory


class ProductDiscountAdmin(BaseDiscountAdmin):
    inlines = [ProductInline, CategoryInline]


class ProductPackInline(BaseInline):
    model = DiscountedPackProduct


class CategoryPackInline(BaseInline):
    model = DiscountedPackCategory


class PackDiscountAdmin(BaseDiscountAdmin):
    inlines = [ProductPackInline, CategoryPackInline]
    list_display = BaseDiscountAdmin.list_display + ['valid_discount']

    def valid_discount(self, obj):
        valid = check_valid_pack_discount(obj)
        return valid
    valid_discount.short_description = _('валидная скидка')


class CartDiscountAdmin(BaseDiscountAdmin):
    list_display = BaseDiscountAdmin.list_display + ['condition', 'condition_value']

    def condition_value(self, obj: CartDiscount) -> str:
        return f'{obj.condition_min_value}-{obj.condition_max_value}'

    condition_value.short_description = _('Значение условия')


admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(PackDiscount, PackDiscountAdmin)
admin.site.register(CartDiscount, CartDiscountAdmin)

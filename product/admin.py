from django.contrib import admin

from .models import Product, Review, Image, Property, ProductProperty


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug', 'views']
    inlines = [ImageInline]
    list_display = ['id', 'category', 'name', 'slug']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ['product', 'property', 'value']


admin.site.register(Product, ProductAdmin)

admin.site.register(Review)

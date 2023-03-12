from product.models import Product

from . import services


class CatalogView(services.CatalogProductService):
    """Представление страницы каталога"""
    template_name = 'catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 2


class CatalogOrderByDateView(services.CatalogProductOrderByService, CatalogView):
    """Представление страницы каталога с отсортированными продуктами по дате"""
    field = 'created_at'


class CatalogOrderByViewsView(services.CatalogProductOrderByService, CatalogView):
    """Представление страницы каталога с отсортированными продуктами по просмотрам"""
    field = 'views'


class CatalogOrderByPriceView(services.CatalogProductOrderByService, CatalogView):
    """Представление страницы каталога с отсортированными продуктами по цене"""
    field = 'shop_products__price'


class CatalogOrderByRatingView(services.CatalogProductOrderByService, CatalogView):
    """Представление страницы каталога с отсортированными продуктами по популярности"""
    field = 'reviews__rating'


class CatalogCategoryView(services.CatalogCategoryService):
    """Представление страницы каталога с категорией продуктов"""
    template_name = 'catalog.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 2


class CatalogCategoryOrderByDateView(services.CatalogCategoryOrderByService, CatalogCategoryView):
    """Представление страницы каталога с категорией продуктов отсортированные по дате"""
    field = 'created_at'


class CatalogCategoryOrderByViewsView(services.CatalogCategoryOrderByService, CatalogCategoryView):
    """Представление страницы каталога с категорией продуктов отсортированные по просмотрам"""
    field = 'views'


class CatalogCategoryOrderByPriceView(services.CatalogCategoryOrderByService, CatalogCategoryView):
    """Представление страницы каталога с категорией продуктов отсортированные по цене"""
    field = 'shop_products__price'


class CatalogCategoryOrderByRatingView(services.CatalogCategoryOrderByService, CatalogCategoryView):
    """Представление страницы каталога с категорией продуктов отсортированные по популярности"""
    field = 'reviews__rating'

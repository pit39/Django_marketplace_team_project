from product.models import Product

from . import services


class CompareView(services.CompareServices):
    model = Product
    template_name = 'compare/compare.html'

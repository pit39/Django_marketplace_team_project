from django.urls import path
from .views import DiscountsView, ProductDiscountView, PackDiscountView, CartDiscountView

urlpatterns = [
    path('', DiscountsView.as_view(), name="discounts"),
    path('product_discounts/<int:pk>', ProductDiscountView.as_view(), name="product-discount"),
    path('pack_discounts/<int:pk>', PackDiscountView.as_view(), name="pack-discount"),
    path('cart_discounts/<int:pk>', CartDiscountView.as_view(), name="cart-discount")
]

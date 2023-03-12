from django.urls import path
from .views import cart_add, CartView, cart_remove, change_count


app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_pk>/', cart_add, name='random_add'),
    path('add/<int:product_pk>/<int:shop_product_pk>/', cart_add, name='add'),
    path('change/<int:shop_product_pk>/<str:quantity>/', change_count, name='change'),
    path('remove/<int:pk>/', cart_remove, name='remove'),
]

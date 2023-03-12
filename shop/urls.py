from django.urls import path
from .views import (
    ShopAllView,
    ShopDetailView,
    CreateShopView,
    AddGoodView,
    EditShopView,
    EditGoodView,
    ShopRoomView,
    ShopRoomDetailView,
)

urlpatterns = [
    path("", ShopAllView.as_view(), name="shops"),
    path("<int:shop_pk>/", ShopDetailView.as_view(), name="shop"),
    path("create/shop/", CreateShopView.as_view(), name="create-shop"),
    path("create/good/", AddGoodView.as_view(), name="create-good"),
    path("edit/shop/<int:shop_pk>/", EditShopView.as_view(), name="edit-shop"),
    path("edit/good/<int:good_pk>", EditGoodView.as_view(), name="edit-good"),
    path("seller-room/", ShopRoomView.as_view(), name="seller-room"),
    path("seller-room/shop/<int:shop_pk>/", ShopRoomDetailView.as_view(), name="seller-shop"),
]

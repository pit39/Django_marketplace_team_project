from django.urls import path
from .views import ProductDetail, ProductCreateView


urlpatterns = [
    path("<str:slug>/", ProductDetail.as_view(), name='product'),
    path("product/create/", ProductCreateView.as_view(), name='create-product'),
]

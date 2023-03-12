from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from config.settings.base import SHOPS_VIEW
from .services import ShopServices
from .models import Shop, ShopProduct
from .forms import CreateShop, AddProductToTheShop, EditShop, EditProductInTheShop


# Create your views here.


class ShopAllView(ShopServices, ListView):
    model = Shop
    template_name = "inc/shop/shops.html"
    paginate_by = SHOPS_VIEW
    context_object_name = "shops"

    def get_queryset(self):
        return self.get_all_shops()


class ShopDetailView(DetailView):
    model = Shop
    template_name = "inc/shop/shop_info.html"
    context_object_name = "shop"
    pk_url_kwarg = "shop_pk"
    paginate_by = SHOPS_VIEW


class ShopRoomView(ShopServices, ListView):
    model = Shop
    template_name = "inc/shop/seller_home.html"
    context_object_name = "shops"
    paginate_by = SHOPS_VIEW

    def get_queryset(self):
        return self.get_user_shop(user=self.request.user)


class ShopRoomDetailView(DetailView):
    model = Shop
    template_name = "inc/shop/seller_shop.html"
    context_object_name = "shop"
    pk_url_kwarg = "shop_pk"
    paginate_by = SHOPS_VIEW


class CreateShopView(ShopServices, View):
    template_name = "inc/shop/create_shop.html"

    def get(self, request):
        form = CreateShop()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CreateShop(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("seller-room")
        return render(request, self.template_name, {"form": form})


class AddGoodView(ShopServices, View):
    template_name = "inc/shop/create_good.html"

    def get(self, request):
        context = {
            "goods": self.get_all_goods(),
            "shops": self.get_user_shop(user=request.user),
            "form": AddProductToTheShop(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = AddProductToTheShop(request.POST)
        if form.is_valid():
            form.save()
            return redirect("seller-room")
        return render(request, self.template_name, {"form": form})


class EditShopView(ShopServices, DetailView):
    context_object_name = "shop"
    model = Shop
    template_name = "inc/shop/edit_shop.html"
    pk_url_kwarg = "shop_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = EditShop(instance=self.get_object())
        return context

    def post(self, request, shop_pk):
        form = EditShop(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect("seller-room")
        return redirect(reverse("edit-shop", kwargs={"shop_pk": shop_pk}))


class EditGoodView(ShopServices, DetailView):
    context_object_name = "good"
    template_name = "inc/shop/edit_good.html"
    model = ShopProduct
    pk_url_kwarg = "good_pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = EditProductInTheShop(instance=self.get_object())
        return context

    def post(self, request, good_pk):
        form = EditProductInTheShop(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect("seller-room")
        return redirect(reverse("edit-shop", kwargs={"good_pk": good_pk}))

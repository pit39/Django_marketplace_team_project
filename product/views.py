from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from personal_account.services import PersonalAccount
from .models import Product, Review
from .forms import CreateProductForm
from .services import ProductService
from cart.forms import CartAddProductForm


class ProductDetail(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product/product.html"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("reviews__user", "shop_products__store", "images")
        return queryset

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["user_review"] = ProductService.user_has_review(self.request.user, self.object)
        context["form"] = CartAddProductForm()
        reviews = Review.objects.filter(product=self.object)
        paginator = Paginator(reviews, 1)
        page = self.request.GET.get("page")
        context["reviews"] = paginator.get_page(page)
        context["paginator"] = paginator
        return context

    def get(self, request, *args, **kwargs):
        ProductService.views_increment(self)
        PersonalAccount.add_viewed_product(user=request.user.id, product=self.get_object().id)
        return super(ProductDetail, self).get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        ProductService.review_form_save(instance=self, request=request)
        return redirect(reverse(viewname="product", kwargs={"slug": self.kwargs["slug"]}))


class ProductCreateView(ProductService, View):
    template_name = "product/create_product.html"

    def get(self, request):
        form = CreateProductForm()
        categories = self.get_all_categories
        return render(request, self.template_name, {"form": form, "categories": categories})

    def post(self, request):
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("seller-room"))
        return render(request, self.template_name, {"form": form})

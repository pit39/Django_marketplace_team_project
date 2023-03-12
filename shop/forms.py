from django import forms
from .models import Shop, ShopProduct


class CreateShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = "__all__"


class AddProductToTheShop(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = "__all__"


class EditShop(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ("name", "address", "email", "phone", "logo")


class EditProductInTheShop(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ("old_price", "price", "amount")

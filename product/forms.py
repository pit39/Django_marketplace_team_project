from django import forms
from .models import Review, Product


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text", "rating"]


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "slug", "category", "description", "sort_index")

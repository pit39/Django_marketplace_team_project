from django import forms
from .models import Order


class StepOneForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            "first_second_names": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": "Введите имя и фамилию",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": "Введите телефон",
                    "required": True,
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": "Введите почту",
                    "required": True,
                }
            ),
        }
        fields = ["first_second_names", "phone", "email"]


class StepTwoForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            "delivery": forms.RadioSelect(attrs={"class": "toggle-box"}),
            "city": forms.TextInput(attrs={
                "class": "form-input border-custom",
                "placeholder": "Введите город",
                "required": True
                }
            ),
            "address": forms.Textarea(attrs={
                "class": "form-textarea border-custom",
                "placeholder": "Введите адрес",
                "required": True
            }),
        }
        fields = ["delivery", "city", "address"]


class StepThreeForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            "payment": forms.RadioSelect(attrs={"class": "toggle-box"}),
        }
        fields = [
            "payment",
        ]

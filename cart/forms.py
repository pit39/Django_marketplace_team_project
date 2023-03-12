from django import forms


class CartAddProductForm(forms.Form):
    """Форма для добавления товара в корзину"""
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'Amount-input form-input', 'value': 1}))

    def clean_quantity(self):
        """Функция проверяет, что поле является числом"""
        data = self.cleaned_data['quantity']
        try:
            data = int(data)
            return data
        except ValueError:
            pass

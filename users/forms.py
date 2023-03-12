from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'phone_number', 'full_name', 'avatar', )


class ResetPasswordForm(forms.Form):

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise ValidationError(message=_('Пользователь не найден'))

        return email


class LogInForm(forms.Form):
    """Форма для авторизации"""
    email = forms.EmailField()
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError(message=_('Не найдено пары E-mail/пароль'))

        return user

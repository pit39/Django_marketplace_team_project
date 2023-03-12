from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView

from personal_account.models import ViewsHistory
from personal_account.services import PersonalAccount
from users.forms import CustomUserCreationForm, ResetPasswordForm, LogInForm

from .services import register_user, password_change, login_user


def register_view(request):
    """Представление с регистрацией пользователя"""
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            register_user(request, user_form=form)

            return redirect(to='main_page')

    return render(request, template_name='users/register.html', context={'form': form})


def user_login(request):
    """Представление с авторизацией пользователя"""
    form = LogInForm()

    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            login_user(request, form)

            return redirect(to='main_page')

    return render(request, 'users/login.html', {'form': form})


class LogOutView(LogoutView):
    template_name = 'users/logout.html'


def reset_password(request):
    """Представление с регистрацией пользователя"""
    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            password_change(request, user_form=form)
            # Здесь будет редирект на главную
            return HttpResponse('Заглушка.'
                                'Ваш новый пароль qwerty1234.')

    return render(request, template_name='users/reset_password.html', context={'form': form})


class HistoryView(View):
    def get(self, request):
        viewed_products = PersonalAccount.get_last_viewed(request.user.id)
        context = {
            'viewed_products': viewed_products
        }
        return render(request, 'users/view_history.html', context)


def history_remove(request, pk: int):
    """Представление удаления товара из списка просмотренных"""
    PersonalAccount.delete_viewed_product(request.user.id, int(pk))
    return redirect(to='users:view_history')

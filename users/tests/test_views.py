from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from users.models import CustomUser
from administration.models import Cache


class RegisterViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='customer').save()
        Cache.objects.create(name='Main cache', value=86400)
        cls.page_name = reverse(viewname='users:register')

        cls.user = {
            'email': 'test@ya.ru',
            'password1': 'TestPass12',
            'password2': 'TestPass12',
        }
        cls.user_short_password = {
            'email': 'test@ya.ru',
            'password1': 'Test',
            'password2': 'Test'
        }
        cls.user_different_passwords = {
            'email': 'test@ya.ru',
            'password1': 'TestPass12',
            'password2': 'TestPass15'
        }

    def setUp(self):
        self.get_response = self.client.get(self.page_name)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/my/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'users/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.page_name, self.user)
        user = CustomUser.objects.get(email='test@ya.ru')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(user.email, 'test@ya.ru')

    def test_add_user_to_customer_group(self):
        self.client.post(self.page_name, self.user)
        user = CustomUser.objects.get(email='test@ya.ru')

        self.assertTrue(user.groups.filter(name='customer').exists())

    def test_cant_register(self):
        response = self.client.post(self.page_name, self.user_short_password)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 0)

        response = self.client.post(self.page_name, self.user_different_passwords)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_redirect_after_register(self):
        response = self.client.post(self.page_name, self.user)
        self.assertRedirects(response, reverse('main_page'))

    def test_authenticated_after_register(self):
        self.client.post(self.page_name, self.user)
        response = self.client.get(self.page_name)
        self.assertTrue(response.context['user'].is_authenticated)


class LogInTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cache.objects.create(name='Main cache', value=86400)
        data = {'email': 'test@ya.ru', 'password': 'test1'}
        cls.user = CustomUser.objects.create_user(email=data['email'], password=data['password'])
        cls.invalid_data = {'email': 'test@ya.ru', 'password': 'test'}
        cls.data = data
        cls.page_name = reverse(viewname='users:login')

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/my/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        response = self.client.get(self.page_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_authenticate(self):
        response = self.client.post(self.page_name, data=self.data)
        self.assertRedirects(response, expected_url=reverse(viewname='main_page'), status_code=302)
        self.assertTrue(self.client.request().context['user'].is_authenticated)

    def test_invalid_authenticate(self):
        response = self.client.post(self.page_name, data=self.invalid_data)
        self.assertContains(response, text='Не найдено пары E-mail/пароль')


class LogOutTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page_name = reverse(viewname='users:logout')

    def setUp(self):
        self.get_response = self.client.get(self.page_name)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/my/logout/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'users/logout.html')


class ResetPasswordTestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.page_name = reverse(viewname='users:reset_password')
        CustomUser.objects.create_user(email='test@ya.ru', password='test1')

    def setUp(self):
        self.get_response = self.client.get(self.page_name)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/my/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'users/reset_password.html')

    def test_reset_password(self):
        response = self.client.post(self.page_name, data={'email': 'test@ya.ru'})
        self.assertEqual(response.status_code, 200)
        user = CustomUser.objects.get(email='test@ya.ru')
        self.assertTrue(user.check_password('qwerty1234'))

    def test_try_reset_password_with_invalid_email(self):
        response = self.client.post(self.page_name, data={'email': 'invalid_mail@ya.ru'})
        self.assertContains(response, text='Пользователь не найден')

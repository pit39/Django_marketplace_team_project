from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(email='admin@ya.ru', password='admin')

    def test_labels(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertIn(field_label, ('e-mail', 'электронная почта'))

        field_label = self.user._meta.get_field('phone_number').verbose_name
        self.assertEqual(field_label, 'телефон')

        field_label = self.user._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'ФИО')

        field_label = self.user._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'аватар')

        field_label = self.user._meta.get_field('is_staff').verbose_name
        self.assertEqual(field_label, 'работник')

        field_label = self.user._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'флаг активности')

    def test_str_method(self):
        self.assertEqual(str(self.user), 'admin@ya.ru')

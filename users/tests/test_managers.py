from django.test import TestCase

from users.models import CustomUser


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user_model = CustomUser
        user = user_model.objects.create_user(email='admin@ya.ru', password='admin')
        self.assertEqual(user.email, 'admin@ya.ru')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='', password="admin")

        self.assertEqual(user_model.objects.get(email='admin@ya.ru'), user)

    def test_create_superuser(self):
        user_model = CustomUser
        admin_user = user_model.objects.create_superuser(email='admin@ya.ru', password='admin')
        self.assertEqual(admin_user.email, 'admin@ya.ru')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)

        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='admin@ya.ru', password='admin@ya.ru', is_superuser=False)

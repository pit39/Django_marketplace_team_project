from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from cart.models import ProductInCart
from administration.models import Cache
from fixtures.test_services.services import create_product, create_user, create_shop, create_shop_product


class CartDetailViewTest(TestCase):
    def setUp(self):
        self.get_response = self.client.get(reverse(viewname='cart:cart'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'cart.html')


class CartAddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cache.objects.create(name='Main cache', value=86400)
        product = create_product()
        user = create_user()
        shop = create_shop(user)
        shop_product = create_shop_product(shop, product)
        shop_2 = create_shop(user=create_user(email='test2@ya.ru'))
        shop_product_2 = create_shop_product(shop_2, product)

        cls.user = user
        cls.product = product
        cls.shop_product = shop_product
        cls.page_name_add = reverse(
            viewname='cart:add',
            kwargs={'product_pk': product.id, 'shop_product_pk': shop_product.id}
        )
        cls.page_name_add_2 = reverse(
            viewname='cart:add',
            kwargs={'product_pk': product.id, 'shop_product_pk': shop_product_2.id}
        )
        cls.page_name_random_add = reverse(
            viewname='cart:random_add',
            kwargs={'product_pk': product.pk}
        )

    def test_cart_add(self):
        """Тест корректности добавления товара в корзину, тест слияния корзины после авторизации"""
        ProductInCart.objects.create(user=self.user, shop_product=self.shop_product, quantity=1)

        response = self.client.post(self.page_name_add, data={'quantity': 1})
        self.assertRedirects(
            response=response,
            expected_url=reverse(viewname='product', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(len(self.client.session['cart']), 1)

        self.client.post(path=reverse(viewname='users:login'), data={'email': 'test@ya.ru', 'password': 'test1'})
        user_cart = self.user.user_carts
        self.assertEqual(user_cart.count(), 1)
        self.assertEqual(user_cart.all()[0].quantity, 2)

    def test_save_cart_after_register(self):
        """Тест переноса корзины после регистрации"""
        self.client.post(self.page_name_add, data={'quantity': 1})
        Group.objects.create(name='customer').save()
        self.client.post(
            path=reverse(viewname='users:register'),
            data={'email': 'test_user@ya.ru', 'password1': 'TestPass123', 'password2': 'TestPass123'}
        )
        user = self.client.request().context['user']
        self.assertEqual(user.user_carts.count(), 1)

    def test_change_seller(self):
        """Тест смены продавца в корзине при добавлении в корзину товара от другого продавца"""
        self.client.force_login(user=self.user)
        self.client.get(self.page_name_add)
        seller_1 = self.user.user_carts.all()[0].shop_product.id
        self.client.get(self.page_name_add_2)
        seller_2 = self.user.user_carts.all()[0].shop_product.id

        self.assertNotEqual(seller_1, seller_2)

    def test_cart_random_add(self):
        """
        Тест добавления товара в корзину без выбора продавца
        """
        self.client.force_login(user=self.user)
        self.client.post(path=self.page_name_random_add, data={'quantity': 1})
        self.assertEqual(self.user.user_carts.count(), 1)

    def test_cart_random_add_invalid_quantity_value(self):
        """Тест не добавления товара в корзину без выбора продавца с невалидным значением кол-ва"""
        self.client.force_login(user=self.user)
        self.client.post(path=self.page_name_random_add, data={'quantity': 'q'})
        self.assertEqual(self.user.user_carts.count(), 0)

    def test_save_cart_after_logout(self):
        """Тест сохранения корзины пользователя после выхода из системы"""
        self.client.force_login(user=self.user)
        self.client.post(self.page_name_add, data={'quantity': 1})
        self.client.logout()

        self.assertEqual(self.user.user_carts.count(), 1)


class CartRemoveViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = create_user()
        product = create_product()
        shop_product = create_shop_product(create_shop(user), product)

        cls.user = user
        cls.page_name_delete = reverse(viewname='cart:remove', kwargs={'pk': product.id})
        cls.page_name_add = reverse(
            viewname='cart:add',
            kwargs={
                'product_pk': product.id,
                'shop_product_pk': shop_product.id
            })

    def test_cart_remove_post(self):
        """Тест корректности удаления товара из корзины"""
        self.client.post(self.page_name_add, data={'quantity': 1})
        response = self.client.post(self.page_name_delete)

        self.assertRedirects(response, reverse('cart:cart'))
        self.assertEqual(len(self.client.session['cart']), 0)

    def test_cart_remove_product_that_not_in_cart(self):
        """Тест появления ошибки при попытке удалить товар, которого нет в корзине у пользователя"""
        self.client.force_login(user=self.user)
        response = self.client.post(self.page_name_delete)

        self.assertEqual(response.status_code, 404)


class CartChangeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        product = create_product()
        user = create_user()
        shop = create_shop(user)
        shop_product = create_shop_product(shop, product)

        cls.product = product
        cls.shop_product = shop_product

        cls.page_name_add = reverse(
            viewname='cart:add',
            kwargs={'product_pk': product.id, 'shop_product_pk': shop_product.id}
        )
        cls.page_name_change = reverse(
            viewname='cart:change',
            kwargs={'shop_product_pk': shop_product.id, 'quantity': '-1'}
        )

    def test_change_count_product_that_not_in_cart(self):
        """Тест появления ошибки при попытке изменить кол-во товара, которого нет в корзине или нет вообще"""
        response = self.client.get(self.page_name_change)
        self.assertEqual(response.status_code, 404)

    def test_change_count(self):
        """Тест корректности изменения кол-ва товара в корзине"""
        self.client.post(self.page_name_add, data={'quantity': 1})
        response = self.client.get(
            reverse(
                viewname='cart:change',
                kwargs={'shop_product_pk': self.shop_product.id, 'quantity': '+1'}
            ))
        self.assertRedirects(response, expected_url=reverse('cart:cart'))
        self.assertEqual(self.client.session['cart'][str(self.product.pk)]['quantity'], 2)

    def test_delete_product(self):
        """Тест корректности удаления товара из корзины при изменении кол-ва до 0"""
        self.client.post(self.page_name_add, data={'quantity': 1})
        response = self.client.get(self.page_name_change)

        self.assertRedirects(response, expected_url=reverse('cart:cart'))
        self.assertEqual(len(self.client.session['cart']), 0)

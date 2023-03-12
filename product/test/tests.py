from django.test import TestCase
from django.urls import reverse

from shop.models import Shop, ShopProduct
from users.models import CustomUser
from product.models import Product
from category.models import Category


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        data = {
            'name': 'test',
            'slug': 'test',
            'category': Category.objects.create(name='test', image='category.svg'),
            'description': 'test_text',
        }

        user = CustomUser.objects.create_user(email='admin@ya.ru', password='TestPass12')
        shop = Shop.objects.create(name='test', holder=user, address='test',
                                   email='test@ya.ru', logo='logo.svg')
        product = Product.objects.create(**data)
        ShopProduct.objects.create(store=shop, product=product, price=1, old_price=2, amount=1)

        cls.user = user
        cls.product = product
        cls.product_url = reverse('product', kwargs={'slug': product.slug})

    def test_product_view(self) -> None:
        response = self.client.get(self.product_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')

    def test_add_review(self) -> None:
        self.client.force_login(user=self.user)
        response = self.client.post(self.product_url, data={'text': 'testreviewtext', 'rating': 3})

        self.assertRedirects(response, expected_url=self.product_url)
        self.assertEqual(self.user.reviews.count(), 1)
        self.assertEqual(self.product.reviews.count(), 1)

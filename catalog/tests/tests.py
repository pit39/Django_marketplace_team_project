from django.test import TestCase
from django.urls import reverse

from product.models import Product
from category.models import Category


class CatalogTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(
            name='test_name',
            image='file.svg'
        )
        cls.products = Product.objects.bulk_create(
            [Product(
                name='test_name_{}'.format(_),
                slug='test-name-{}'.format(_),
                category=cls.category,
            ) for _ in range(10)]
        )
        cls.categories: list = [Category.objects.create(
            name='test_name_{}'.format(_),
            image='file_{}.svg'
        ) for _ in range(10)]

    def test_catalog_get(self) -> None:
        response = self.client.get(reverse('catalog'))
        self.assertTrue(response.status_code == 200)

    def test_catalog_add_to_compare(self) -> None:
        for i, product in enumerate(self.products):
            with self.subTest(i=i):
                response = self.client.get(reverse('add_to_compare', kwargs={'pk': i}))
                self.assertTrue(response.status_code == 302)

    def test_catalog_template(self) -> None:
        response = self.client.get(reverse('catalog'))
        self.assertTemplateUsed(response, 'catalog.html')

    def test_catalog_category_get(self):
        for i, category in enumerate(self.categories):
            with self.subTest(i=i):
                response = self.client.get(reverse('catalog_category', kwargs={'slug': category.slug}))
                self.assertTrue(response.status_code == 200)

    def test_catalog_category_template(self):
        for i, category in enumerate(self.categories):
            with self.subTest(i=i):
                response = self.client.get(reverse('catalog_category', kwargs={'slug': category.slug}))
                self.assertTemplateUsed(response, 'catalog.html')

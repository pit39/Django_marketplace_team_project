from django.test import TestCase
from django.urls import reverse


class ComposeTestCase(TestCase):
    def setUp(self) -> None:
        session = self.client.session
        session['compare'] = [_ for _ in range(10)]
        session.save()

    def test_compare_get(self):
        response = self.client.get(reverse('compare'))
        self.assertTrue(response.status_code == 200)

    def test_compare_template(self) -> None:
        response = self.client.get(reverse('compare'))
        self.assertTemplateUsed(response, 'compare/compare.html')

    def test_compare_delete_redirect(self) -> None:
        response = self.client.get(reverse('delete_from_compare', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('compare'))

    def test_compare_delete_session(self) -> None:
        self.client.get(reverse('delete_from_compare', kwargs={'pk': 1}))
        self.assertTrue(1 not in self.client.session.get('compare'))

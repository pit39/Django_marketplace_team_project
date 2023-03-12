from django.shortcuts import redirect, render
from django.urls import reverse

from django.db.models import Model
from django.views import View

from typing import Optional


class CompareServices(View):

    model: Optional[Model] = None
    template_name: Optional[str] = None

    def get(self, request):
        objects_ = self.model.objects.prefetch_related('property').filter(pk__in=request.session.get('compare', []))
        context = {'{}s'.format(self.model.__name__.lower()): objects_}
        return render(request, self.template_name, context)

    def delete_from_compare(self, pk):
        """Удаление товара из списка сравнения"""
        products_pk: list = self.session.get('compare')
        products_pk.remove(pk)
        self.session['compare'] = products_pk
        return redirect(reverse('compare'))

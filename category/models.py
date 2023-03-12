from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from . import utility
from . import tools


class Category(utility.StrMixin, MPTTModel):
    """Категории продуктов"""
    name = models.CharField(max_length=128, unique=True, verbose_name=_('наименование'))
    slug = models.SlugField(max_length=256, blank=True, verbose_name=_('slug'))
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('родитель'))
    image = models.FileField(upload_to=tools.get_path, verbose_name=_('иконка'))

    def save(self, *args, **kwargs):
        self.slug = tools.get_slug(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

from django.db import models
from django.utils.translation import gettext_lazy as _


class Cache(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        db_table = 'Cache_time'
        verbose_name = _('кэширование')

    def __str__(self):
        return self.name

from django.contrib import admin
from . import models


@admin.register(models.ViewsHistory)
class ViewsHistoryModelAdmin(admin.ModelAdmin):
    pass


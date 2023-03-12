from django.contrib import admin

from .models import Cache


class CacheAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


admin.site.register(Cache, CacheAdmin)

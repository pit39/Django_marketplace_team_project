from django.contrib import admin

from main_page.models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ['product', 'description', 'logo']


admin.site.register(Banner, BannerAdmin)

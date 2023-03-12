"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('product/compare/', include('compare.urls')),
    path('product/', include('product.urls')),
    path('', include('main_page.urls')),
    path('my/', include('users.urls', namespace='users')),
    path('shops/', include('shop.urls')),
    path('account/', include('personal_account.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('discounts/', include('discount.urls')),
    path('import_data/', include('import_data.urls')),
    path('order/', include('order.urls')),
    path('pay/', include('payment.urls', namespace='payment')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

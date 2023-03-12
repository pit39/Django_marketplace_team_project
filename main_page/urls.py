from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('contacts/', views.ContactsView.as_view(), name='contacts')
]

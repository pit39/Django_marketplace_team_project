from django.urls import path

from . import views


urlpatterns = [
    path('', views.CompareView.as_view(), name='compare'),
    path('delete_from_compare/<int:pk>/', views.CompareView.delete_from_compare, name='delete_from_compare'),
]

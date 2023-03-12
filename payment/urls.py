from django.urls import path

from .views import PaymentAPIView


app_name = 'payment'

urlpatterns = [
    path('<int:card_number>/<str:cost>/', PaymentAPIView.as_view(), name='pay'),
]

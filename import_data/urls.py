from django.urls import path

from . import views


urlpatterns = [
    path('', views.ImportDataView.as_view(), name='import_data'),
]

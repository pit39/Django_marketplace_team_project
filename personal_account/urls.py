from django.urls import path
from .views import AccountView, ProfileView

urlpatterns = [
    path("", AccountView.as_view(), name="account"),
    path("profile/", ProfileView.as_view(), name="profile"),
]

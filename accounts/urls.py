from django.urls import path
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    RefreshView,
    LogoutView,
    MeView,
    DeleteAccountView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("delete/", DeleteAccountView.as_view()),
]
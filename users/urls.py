from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.permissions import AllowAny

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="get_token"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("create/", views.UserCreateAPIView.as_view(), name="create"),
    path("", views.UserRetrieveUpdateAPIView.as_view(), name="profile"),
    path("upd-pass/", views.UserPasswordUpdateAPIView.as_view(), name="update-password"),
]

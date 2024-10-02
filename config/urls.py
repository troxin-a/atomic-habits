from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls", namespace="users")),
    path("habit/", include("habits.urls", namespace="habits")),
]

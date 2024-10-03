from django.urls import path
from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("", views.HabitListCreateAPIView.as_view(), name="list-create"),
    path("public/", views.HabitPublicListAPIView.as_view(), name="list-public"),
    path("<int:pk>/", views.HabitRetrieveUpdateDestroyAPIView.as_view(), name="retrieve-update-destroy"),
]

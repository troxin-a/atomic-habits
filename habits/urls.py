from django.urls import path
from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("", views.HabitCreateAPIView.as_view(), name="create"),
]

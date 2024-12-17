from django.urls import path

from task_tracker.views import index

urlpatterns = [
    path("", index, name="index"),
]


app_name = "task_tracker"
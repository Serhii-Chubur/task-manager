from django.urls import path

from task_tracker.views import (index,
                                TaskDetailView,
                                DashboardView,
                                task_completed,
                                TaskCreateView,
                                TaskUpdateView,
                                TaskDeleteView)

urlpatterns = [
    path("", index, name="index"),
    path("dashboard/<int:pk>", DashboardView.as_view(), name="dashboard"),
    path("task-detail/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("task-detail/<int:pk>/complete", task_completed, name="task-complete"),
    path("task-create/", TaskCreateView.as_view(), name="task-create"),
    path("task-update/<int:pk>", TaskUpdateView.as_view(), name="task-update"),
    path("task-delete/<int:pk>", TaskDeleteView.as_view(), name="task-delete"),
]


app_name = "task_tracker"
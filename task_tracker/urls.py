from django.urls import path

from task_tracker.views import (TaskDetailView,
                                DashboardView,
                                TaskCreateView,
                                TaskUpdateView,
                                TaskDeleteView,
                                WorkerUpdateView,
                                WorkerDeleteView,
                                WorkerDetailView,
                                IndexView, TaskCompletedView)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dashboard/<int:pk>/",
         DashboardView.as_view(),
         name="dashboard"),
    path("task-detail/<int:pk>/",
         TaskDetailView.as_view(),
         name="task-detail"),
    path("task-detail/<int:pk>/complete/",
         TaskCompletedView.as_view(),
         name="task-complete"),
    path("task-create/",
         TaskCreateView.as_view(),
         name="task-create"),
    path("task-update/<int:pk>/",
         TaskUpdateView.as_view(),
         name="task-update"),
    path("task-delete/<int:pk>/",
         TaskDeleteView.as_view(),
         name="task-delete"),
    path("worker-update/<int:pk>/",
         WorkerUpdateView.as_view(),
         name="worker-update"),
    path("worker-delete/<int:pk>/",
         WorkerDeleteView.as_view(),
         name="worker-delete"),
    path("worker-detail/<int:pk>/",
         WorkerDetailView.as_view(),
         name="worker-detail"),
]


app_name = "task_tracker"

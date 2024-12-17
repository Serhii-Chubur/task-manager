from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from task_tracker.models import Position, Worker, Task


# Create your views here.
def index(request:HttpRequest) -> HttpResponse:
    positions = Position.objects.all().count()
    users = Worker.objects.all().count()
    tasks = Task.objects.filter(is_completed=False).count()
    context = {
        "positions": positions,
        "users": users,
        "tasks": tasks,
    }
    return render(request, "home/index.html", context=context)

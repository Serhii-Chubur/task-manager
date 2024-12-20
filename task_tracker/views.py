from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login, get_user
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView

from task_tracker.forms import LoginForm, SignUpForm
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

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Account created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



class DashboardView(ListView):
    model = Task
    template_name = "home/dashboard.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = Task.objects.filter(assignees__id=pk, is_completed=False)

        if self.request.GET.get('show_all', 'false') == 'true':
            queryset = Task.objects.filter(assignees__id=pk)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_all'] = self.request.GET.get('show_all', 'false') == 'true'  # Pass the state of the "All" button
        return context


class CreateTaskView(CreateView):
    pass


class TaskDetailView(DetailView):
    model = Task
    template_name = "home/task_detail.html"


def task_completed(request, pk:int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save()
    return redirect("task_tracker:dashboard", get_user(request).pk)

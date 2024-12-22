from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import (CreateView,
                                  DetailView,
                                  ListView,
                                  UpdateView,
                                  DeleteView)

from task_tracker.forms import (LoginForm,
                                SignUpForm,
                                AssigningForm,
                                TaskCreationForm,
                                TaskSearchForm)
from task_tracker.models import Position, Worker, Task


# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse:
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
                msg = "Invalid credentials"
        else:
            msg = "Error validating the form"

    return render(request, "registration/login.html",
                  {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")

        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html",
                  {"form": form, "msg": msg, "success": success})


class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "home/dashboard.html"
    context_object_name = "tasks"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        queryset = Task.objects.filter(assignees__id=pk, is_completed=False)
        form = TaskSearchForm(self.request.GET)

        if self.request.GET.get("show_all", "false") == "true":
            queryset = Task.objects.filter(assignees__id=pk)

        if form.is_valid():
            return Task.objects.filter(
                assignees__id=pk,
                name__icontains=form.cleaned_data["task"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.request.GET.get("task", "")
        context["show_all"] = self.request.GET.get("show_all",
                                                   "false") == "true"
        context["task_search_form"] = TaskSearchForm(
            initial={"task": task}
        )
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "home/task_create.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("task_tracker:dashboard", kwargs={"pk": pk})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "home/task_create.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("task_tracker:dashboard", kwargs={"pk": pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "home/task_detail.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("task_tracker:dashboard", kwargs={"pk": pk})


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "home/task_detail.html"
    form_class = AssigningForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return HttpResponseNotFound("Task not found")
        form = AssigningForm(request.POST)

        if form.is_valid():

            self.object.assignees.set(form.cleaned_data["assignees"])
            self.object.save()
            return redirect("task_tracker:task-detail", pk=self.object.pk)

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        context["assignees"] = task.assignees.all()
        context["form"] = AssigningForm(instance=task)
        return context


@login_required
def task_completed(request, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = True
    task.save()
    return redirect("task_tracker:dashboard", get_user(request).pk)


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "home/worker_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assignees__id=self.request.user.pk)
        context["tasks"] = tasks
        return context


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = SignUpForm
    template_name = "home/worker_update.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("task_tracker:dashboard", kwargs={"pk": pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "home/worker_detail.html"

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse("task_tracker:dashboard", kwargs={"pk": pk})

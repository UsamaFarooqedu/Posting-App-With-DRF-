from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm,SignUpForm

# Authentication Views
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'task/signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Project Views
class HomeView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'task/home.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'task/project-detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'task/project-detail.html'  # <-- use a separate form template
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'task/project-detail.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'task/project_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

# Task Views
@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task-detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(project__created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id, created_by=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm(project=project)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, project__created_by=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=task.project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.id)
    else:
        form = TaskForm(instance=task, project=task.project)
    
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task
    })

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.id})

    def get_queryset(self):
        return Task.objects.filter(project__created_by=self.request.user)

# Comment Views
@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id, project__created_by=request.user)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    
    return redirect('task_detail', pk=task.id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    task_id = comment.task.id
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('task_detail', pk=task_id)
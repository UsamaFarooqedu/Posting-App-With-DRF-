from django.contrib import admin
from .models import Project, Task, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at', 'updated_at']

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['title', 'status', 'due_date', 'created_by', 'assigned_to']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'created_by__username']
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'due_date', 'created_by', 'assigned_to']
    list_filter = ['status', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'project__title']
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'task', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'task__title', 'author__username']
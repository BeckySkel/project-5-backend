from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin for Project model
    """
    list_display = ('title', 'creator', 'updated_on')
    search_fields = ['title', 'creator']
    list_filter = ('created_on', 'updated_on',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin for Task model
    """
    list_display = ('summary', 'creator', 'project', 'updated_on')
    search_fields = ['summary', 'creator', 'body']
    list_filter = ('created_on', 'updated_on', 'due_date')

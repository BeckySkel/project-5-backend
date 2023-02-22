from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin for Project model
    """
    list_display = ('title', 'creator', 'updated_on', 'removed')
    search_fields = ['title', 'creator']
    list_filter = ('created_on', 'updated_on', 'removed', 'private')

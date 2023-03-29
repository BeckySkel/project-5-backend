from django.contrib import admin
from .models import Contributor

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """
    Admin for Contributor model
    """
    list_display = ('user', 'creator', 'project')
    list_filter = ('user', 'creator', 'project',)

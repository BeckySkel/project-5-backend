from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin for Profile model
    """
    list_display = ('user', 'full_name', 'email')
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ('created_on',)

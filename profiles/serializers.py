from rest_framework import serializers
from .models import Profile
from projects.serializers import ProjectSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Checks if profile belongs to current user.
    Displays a created projects list.
    """
    user = serializers.ReadOnlyField(source='user.username')
    is_current_user = serializers.SerializerMethodField()
    created_projects_count = serializers.ReadOnlyField()
    contrib_projects_count = serializers.ReadOnlyField()
    created_projects_list = serializers.SerializerMethodField()

    def get_is_current_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    # https://stackoverflow.com/questions/14639106/how-can-i-retrieve-a-list-of-field-for-all-objects-in-django
    def get_created_projects_list(self, obj):
        return obj.user.projects.all().values_list('title', flat=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'created_on',
            'bio', 'is_current_user', 'created_projects_count',
            'contrib_projects_count', 'created_projects_list'
        ]

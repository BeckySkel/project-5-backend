from rest_framework import serializers
from .models import Profile
from projects.models import Project
from contributors.models import Contributor
from projects.serializers import BasicProjectSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Returns boolean value for if the profile belongs to the current user.
    Displays a created projects list.
    """
    # Profile data
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    email_verified = serializers.ReadOnlyField()

    def get_full_name(self, obj):
        # Name input is optional so only names that exist
        # otherwise returns empty string
        names = []
        for name in [obj.first_name, obj.last_name]:
            if len(name):
                names.append(name)
        return ' '.join(names)

    def get_email(self, obj):
        return obj.user.email

    # Project data
    created_projects_count = serializers.ReadOnlyField()
    created_projects = BasicProjectSerializer(
        many=True,
        read_only=True,
        source='user.projects'
        )
    contrib_projects_count = serializers.ReadOnlyField()
    contrib_projects = serializers.SerializerMethodField()

    def get_contrib_projects(self, obj):
        contributing_to = Contributor.objects.filter(
            user_id=obj.user_id
            ).values_list('project_id', flat=True)
        return Project.objects.filter(id__in=contributing_to).values(
            'id',
            'title',
            'creator'
            )

    # User boolean data
    is_current_user = serializers.SerializerMethodField()

    def get_is_current_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_id', 'first_name', 'last_name', 'full_name',
            'email', 'email_verified', 'bio', 'menu_open', 'created_on',
            'created_projects_count', 'created_projects',
            'contrib_projects_count', 'contrib_projects', 'is_current_user',
        ]

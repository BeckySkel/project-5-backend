from rest_framework import serializers
from .models import Project, Task
from contributors.models import Contributor
from django.contrib.auth.models import User


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Validates contributor selection (creator cannot be a contributor).
    Checks if current user is the creator or a contributor.
    Displays task ids and contributor profile ids.
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    task_count = serializers.ReadOnlyField()
    task_ids = serializers.SerializerMethodField()

    contributor_instances = serializers.SerializerMethodField()
    contributor_names = serializers.SerializerMethodField()
    is_contrib = serializers.SerializerMethodField()

    def validate_contributors(self, value):
        request = self.context['request']
        if request.user in value:
            raise serializers.ValidationError('Cannot add self as contributor')
        return value

    def get_contributor_instances(self, obj):
        request = self.context['request']
        return obj.contributor.all().values_list('user', flat=True)

    def get_contributor_names(self, obj):
        request = self.context['request']
        users = obj.contributor.values_list('user', flat=True)
        for user in users:
            return User.objects.filter(id=user).values_list('username', flat=True)

    def get_is_contrib(self, obj):
        request = self.context['request']
        contributors = obj.contributor.all().values_list('user', flat=True)
        return request.user in contributors

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_task_ids(self, obj):
        tasks = obj.tasks.all()
        task_ids = [t.id for t in tasks]
        return task_ids

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'creator', 'profile_id',
            'contributors', 'task_count', 'task_ids',
            'created_on', 'updated_on', 'is_creator',
            'contributor_instances', 'contributor_names', 'is_contrib'
        ]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Validates project selection (user must be project creator or contributor).
    Checks if current user is the creator.
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    is_project_creator = serializers.SerializerMethodField()
    is_project_contrib = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    project_title = serializers.ReadOnlyField(source='project.title')

    def validate_project(self, value):
        user = self.context['request'].user
        project = Project.objects.get(pk=value.id)
        contrib = user in project.contributors.all()
        creator = user == project.creator
        if not contrib and not creator:
            raise serializers.ValidationError('You do not have\
 permission to add tasks to this project')
        return value

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_project_creator(self, obj):
        request = self.context['request']
        return request.user == obj.project.creator

    def get_is_project_contrib(self, obj):
        request = self.context['request']
        return request.user in obj.project.contributors.all()

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_title', 'summary', 'body', 'due_date',
            'completed', 'creator', 'profile_id', 'created_on', 'updated_on',
            'is_creator', 'is_project_creator', 'is_project_contrib'
        ]

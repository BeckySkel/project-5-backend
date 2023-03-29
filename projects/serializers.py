from rest_framework import serializers
from .models import Project, Task
from contributors.models import Contributor
from contributors.serializers import ContributorSerializer
from django.contrib.auth.models import User
import json


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    Returns boolean values for if current user is the creator or a contributor.
    Displays task ids and serialized contributor data.
    """
    # Creator data
    creator = serializers.ReadOnlyField(source='creator.username')
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    # Contributor data
    contrib_count = serializers.ReadOnlyField()
    contributors = ContributorSerializer(many=True, read_only=True)
    # Task data
    task_count = serializers.ReadOnlyField()
    task_ids = serializers.SerializerMethodField()

    def get_task_ids(self, obj):
        tasks = obj.tasks.all()
        task_ids = [t.id for t in tasks]
        return task_ids

    # User boolean data
    is_creator = serializers.SerializerMethodField()
    is_contrib = serializers.SerializerMethodField()

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_contrib(self, obj):
        request = self.context['request']
        return request.user.id in obj.contributors.all()\
            .values_list('user', flat=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'creator', 'profile_id',
            'contrib_count', 'contributors', 'task_count', 'task_ids',
            'created_on', 'updated_on', 'is_creator', 'is_contrib'
        ]


class BasicProjectSerializer(serializers.ModelSerializer):
    """
    Serializer to provide information needed to create project
    navigation links: id, title and creator
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'creator']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Validates project selection (user must be project creator or contributor).
    Returns boolean values for if current user is the creator or contributor
    of the associated project and if current user is creator of the task.
    """
    # Project data
    project_title = serializers.ReadOnlyField(source='project.title')

    def validate_project(self, value):
        user = self.context['request'].user
        project = Project.objects.get(pk=value.id)
        contrib = user.id in project.contributors.all()\
            .values_list('user', flat=True)
        creator = user == project.creator
        if not contrib and not creator:
            raise serializers.ValidationError('You do not have\
 permission to add tasks to this project')
        return value

    # Task Creator data
    creator = serializers.ReadOnlyField(source='creator.username')
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')

    # User boolean data
    is_creator = serializers.SerializerMethodField()
    is_project_creator = serializers.SerializerMethodField()
    is_project_contrib = serializers.SerializerMethodField()

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_project_creator(self, obj):
        request = self.context['request']
        return request.user == obj.project.creator

    def get_is_project_contrib(self, obj):
        request = self.context['request']
        return request.user.id in obj.project.contributors.all()\
            .values_list('user', flat=True)

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_title', 'summary', 'body',
            'completed', 'creator', 'profile_id', 'created_on', 'updated_on',
            'is_creator', 'is_project_creator', 'is_project_contrib'
        ]

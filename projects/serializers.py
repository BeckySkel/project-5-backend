from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    is_contributor = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    def validate_contributors(self, value):
        request = self.context['request']
        if request.user in value:
            raise serializers.ValidationError('Cannot add self as contributor')
        return value

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_contributor(self, obj):
        request = self.context['request']
        return request.user in obj.contributors.all()

    def get_task_count(self, obj):
        return obj.tasks.all().count()

    class Meta:
        model = Project
        fields = [
            'id', 'url_id', 'title', 'description', 'creator', 'profile_id',
            'contributors', 'task_count', 'created_on', 'updated_on',
            'is_creator', 'is_contributor'
        ]


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    project_title = serializers.ReadOnlyField(source='project.title')

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    class Meta:
        model = Task
        fields = [
            'id', 'summary', 'body', 'due_date', 'completed', 'creator',
            'created_on', 'updated_on', 'project', 'project_title',
            'is_creator', 'profile_id'
        ]

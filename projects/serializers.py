from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    is_contributor = serializers.SerializerMethodField()

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

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'url_id', 'description', 'creator', 'contributors',
            'created_on', 'updated_on', 'is_creator', 'profile_id',
            'is_contributor'
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

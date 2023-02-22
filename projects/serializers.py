from rest_framework import serializers
from .models import Project

# Code from CI walkthrough project
class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Project
        fields = [
            'title', 'url_id', 'description', 'creator', 'created_on',
            'updated_on', 'removed', 'private', 'is_owner', 'profile_id'
        ]
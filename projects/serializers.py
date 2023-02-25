from rest_framework import serializers
from .models import Project


# Code from CI walkthrough project
class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    is_creator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    # profile_image = serializers.ReadOnlyField(
    #     source='creator.profile.profile_image.url'
    #     )

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'url_id', 'description', 'creator', 'created_on',
            'updated_on', 'removed', 'private', 'is_creator', 'profile_id',
            # 'profile_image'
        ]
from rest_framework import serializers
from .models import Profile
from projects.serializers import ProjectSerializer


# Code inspired by CI walkthrough project
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_current_user = serializers.SerializerMethodField()
    count_projects = serializers.SerializerMethodField()
    projects_list = serializers.SerializerMethodField()
    # print()
    # projects_list = ProjectSerializer(source='user.projects.all', many=True)

    def get_is_current_user(self, obj):
        request = self.context['request']
        return request.user == obj.user
    
    def get_count_projects(self, obj):
        return obj.user.projects.all().count()

    def get_projects_list(self, obj):
        return obj.user.projects.all().values_list('title')

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'created_on',
            'bio', 'is_current_user', 'count_projects', 'projects_list'
        ]

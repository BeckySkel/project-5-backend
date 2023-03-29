from django.db import IntegrityError
from rest_framework import serializers
from .models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.
    Returns boolean value for if the profile belongs to the current user.
    Displays a created projects list.
    """
    # Contributor data
    user_username = serializers.ReadOnlyField(source='user.username')
    user_profile_id = serializers.ReadOnlyField(source='user.profile.id')

    def validate_user(self, value):
        request = self.context['request']
        print(value)
        if request.user == value:
            raise serializers.ValidationError('Cannot add self as contributor')
        return value

    # Project data
    project_title = serializers.ReadOnlyField(source='project.title')

    def validate_project(self, value):
        request = self.context['request']
        if request.user != value.creator:
            raise serializers.ValidationError(
                'Must be the project creator to add contributors'
                )
        return value

    # Creator data
    creator = serializers.ReadOnlyField(source='creator.id')
    creator_username = serializers.ReadOnlyField(source='creator.username')
    creator_profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    # User boolean data
    is_user = serializers.SerializerMethodField()
    is_project_creator = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_is_project_creator(self, obj):
        request = self.context['request']
        return request.user == obj.project.creator

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'user_username', 'user_profile_id', 'project',
            'project_title', 'creator', 'creator_username',
            'creator_profile_id', 'is_user', 'is_project_creator', 'is_creator'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})

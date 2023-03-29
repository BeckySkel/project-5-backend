from django.db import IntegrityError
from rest_framework import serializers
from .models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model
    """
    user_profile_id = serializers.ReadOnlyField(source='user.profile.id')
    creator = serializers.ReadOnlyField(source='user.id')
    creator_profile_id = serializers.ReadOnlyField(source='creator.profile.id')
    user_username = serializers.ReadOnlyField(source='user.username')
    project_name = serializers.ReadOnlyField(source='project.title')
    is_creator = serializers.SerializerMethodField()
    is_user = serializers.SerializerMethodField()
    creator_username = serializers.ReadOnlyField(source='creator.username')
    is_project_creator = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_project_creator(self, obj):
        request = self.context['request']
        return request.user == obj.project.creator

    def validate_user(self, value):
        request = self.context['request']
        print(value)
        if request.user == value:
            raise serializers.ValidationError('Cannot add self as contributor')
        return value

    def validate_project(self, value):
        request = self.context['request']
        if request.user != value.creator:
            raise serializers.ValidationError(
                'Must be the project creator to add contributors'
                )
        return value

    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'user_username', 'user_profile_id', 'project',
            'project_name', 'creator', 'creator_username',
            'creator_profile_id', 'is_user', 'is_project_creator', 'is_creator'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})

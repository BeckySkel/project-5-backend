from django.db import IntegrityError
from rest_framework import serializers
from .models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model
    """
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    project_name = serializers.ReadOnlyField(source='project.title')
    is_creator = serializers.SerializerMethodField()
    is_contributor = serializers.SerializerMethodField()
    creator = serializers.ReadOnlyField(source='creator.username')
    is_project_creator = serializers.SerializerMethodField()

    def get_is_contributor(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def get_is_project_creator(self, obj):
        request = self.context['request']
        return request.user == obj.project.creator

    def validate_contributor(self, value):
        request = self.context['request']
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
            'id', 'user', 'profile_id', 'project', 'project_name',
            'is_creator', 'is_contributor', 'creator', 'is_project_creator'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})

from django.db import IntegrityError
from rest_framework import serializers
from .models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model
    """
    user = serializers.ReadOnlyField(source='user.username')
    profile_id = serializers.ReadOnlyField(source='user.profile.id')
    project = serializers.ReadOnlyField(source='project.title')
    project_id = serializers.ReadOnlyField(source='project.id')
    is_creator = serializers.SerializerMethodField()
    is_contributor = serializers.SerializerMethodField()

    def get_is_contributor(self, obj):
        request = self.context['request']
        return request.user == obj.user

    def get_is_creator(self, obj):
        request = self.context['request']
        return request.user == obj.creator

    def validate_contributor(self, value):
        request = self.context['request']
        if request.user == value:
            raise serializers.ValidationError('Cannot add self as contributor')
        return value

    class Meta:
        model = Contributor
        fields = [
            'id', 'user', 'profile_id', 'project', 'project_id',
            'is_creator', 'is_contributor'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})

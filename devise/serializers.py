from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


# Code from CI walkthrough project
class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serializer for the current user
    """
    profile_id = serializers.ReadOnlyField(source='profile.id')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id',
        )

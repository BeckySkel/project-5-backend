from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


# Code from CI walkthrough project
class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    # email_verified = serializers.ReadOnlyField(source='profile.email_verified')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id',
            # 'email_verified',
        )

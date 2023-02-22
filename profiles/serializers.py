from rest_framework import serializers
from .models import Profile

# Code from CI walkthrough project
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'profile_image', 'email'
        ]
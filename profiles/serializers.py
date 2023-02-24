from rest_framework import serializers
from .models import Profile

# Code from CI walkthrough project
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_user = serializers.SerializerMethodField()

    def get_is_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'profile_image', 'email',
            'is_user'
        ]
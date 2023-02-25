from rest_framework import serializers
from .models import Profile


# Code from CI walkthrough project
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    is_user = serializers.SerializerMethodField()

    def validate_profile_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image is too large. Profile image can be no larger than 2MB'
            )
        if value.image.width > 4096 or value.image.height > 4096:
            raise serializers.ValidationError(
                'Image is too large. Max image dimensions are 4096px x 4096px'
            )
        return value

    def get_is_user(self, obj):
        request = self.context['request']
        return request.user == obj.user

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'profile_image', 'email',
            'is_user'
        ]

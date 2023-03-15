from rest_framework import permissions


# Custom permission from CI walkthrough project
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an item to edit it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return obj.user == request.user
        except AttributeError:
            return obj.creator == request.user

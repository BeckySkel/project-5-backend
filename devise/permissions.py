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


# Custom permission from CI walkthrough project
class IsContribOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner or contributors of
    an item to edit it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        iscreator = obj.creator == request.user
        try:
            iscontrib = request.user in obj.contributors.all()
        except AttributeError:
            iscreator = obj.project.creator == request.user
            iscontrib = request.user in obj.project.contributors.all()

        permission = iscreator or iscontrib
        return permission


class ContributorDeletionPermission(permissions.BasePermission):
    """
    Custom permission to allow only the owner or contributors of
    an item to edit it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        iscreator = obj.creator == request.user
        isuser = obj.user == request.user

        permission = iscreator or isuser
        return permission

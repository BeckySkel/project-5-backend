from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("lllllllllllllllllllllll")
        if request.method in permissions.SAFE_METHODS:
            return True
        # return obj.user == request.user
        try:
            return obj.user == request.user
        except AttributeError:
            return obj.creator == request.user

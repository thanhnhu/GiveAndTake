from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerOrIsAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # Note that this method just be called for UPDATE/DELETE method
    # And only called if has_permission() has passed.
    def has_object_permission(self, request, view, obj):
        isAdmin = super().has_permission(request, view)
        # Instance must have an attribute named `user`.
        return obj.user == request.user or isAdmin


class IsOwnerOrIsAdminOrReadOnly(IsOwnerOrIsAdmin):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    # Object-level permission to only allow owners of an object to edit it.
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        isOwnerIsAdmin = super().has_object_permission(request, view, obj)
        return isOwnerIsAdmin


class PostOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        isPost = request.method == 'POST'
        isAuthenticated = request.user.is_authenticated
        isAdmin = super().has_permission(request, view)
        if isPost and (isAuthenticated or isAdmin):
            return True
        return False


class DeleteDenied(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return False
        return True

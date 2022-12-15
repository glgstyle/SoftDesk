from rest_framework import permissions


# permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        # print('has_permission')
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            print('true')
            return True
        # Instance must have an attribute named `owner`.
        return obj.author_user == request.user


class IsContributor(permissions.BasePermission):
    """
    Object-level permission to only allow contributors of an object
    to get access to CRUD actions.
    Assumes the model instance has an `contributor` attribute.
    """
    def has_permission(self, request, view):
        # print('has_permission')
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        # return obj.user == request.user
        # print("///////author : ", obj.author, "request.user : ", request.user.id)
        return obj.author == request.user.id

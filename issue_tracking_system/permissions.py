from rest_framework import permissions
from issue_tracking_system.models import Contributor

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
        """Return True if request.user is a contributor 
           and give him permission to modify the project"""
        project = obj.id
        try:
            contributor = Contributor.objects.get(project_id=project, user_id=request.user.id)
        except Contributor.DoesNotExist:
            contributor = None
        if contributor is not None:
            return True
        return False



from rest_framework import permissions
from issue_tracking_system.models import Contributor, Project


# permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named author_user`.
        return obj.author_user == request.user


class IsOwnerOfProject(permissions.BasePermission):
    """
    Object-level permission to only allow owners of project to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        # Retrieve the project_id from view
        project_id = request.resolver_match.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        if (project.author_user == request.user):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsContributor(permissions.BasePermission):
    """
    Object-level permission to only allow contributors of an object
    to get access to CRUD actions.
    Assumes the model instance has an `contributor` attribute.
    """
    def has_permission(self, request, view):
        project_id = request.resolver_match.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        try:
            contributor = Contributor.objects.get(
                project_id=project_id, user_id=request.user.id)
        except Contributor.DoesNotExist:
            contributor = None
        if (contributor is not None) or (project.author_user == request.user):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Return True if request.user is a contributor
           and give him permission to update/delete the contributors
           if he's owner"""

        if request.method in permissions.SAFE_METHODS:
            return self.has_permission(request, view)
        # Instance must have an attribute named author_user`.
        return obj.author_user == request.user

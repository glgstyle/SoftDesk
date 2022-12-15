from issue_tracking_system.models import Project, Contributor, Issue, Comment
from issue_tracking_system.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from authentication.serializers import UsersSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status, generics
from django.shortcuts import get_object_or_404
from authentication.models import User


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

        # Instance must have an attribute named `contributor`.
        return obj.user == request.user


class ProjectViewset(ModelViewSet):
    """View for Project object. """

    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]  # Only for logged users and owner or only read
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """Define the Query String usable in url. """
        queryset = Project.objects.all()
        project = self.request.GET.get('project')
        if project is not None:
            queryset = queryset.filter(id=project)
        return queryset
    
    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user=self.request.user)

    
class ContributorViewset(ModelViewSet):
    """View for Contributor object. """

    permission_classes = [IsAuthenticated & IsContributor] 
    serializer_class = UsersSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        contributor_queryset = Contributor.objects.filter(
            project=self.kwargs['project_pk'])         
        users_ids = contributor_queryset.values_list('user', flat=True)
        queryset = User.objects.filter(pk__in=users_ids).all()
        return queryset

    
class IssueViewset(ModelViewSet):
    """View for Issue object. """

    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly] 
    serializer_class = IssueSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Issue.objects.filter(project=self.kwargs['project_pk'])
        project = self.request.GET.get('project')
        if project is not None:
            queryset = queryset.filter(project__id=project)
        return queryset 
        
    def perform_create(self, serializer):
        # save the request.user as author when creating the issue
        project= Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author_user=self.request.user,
                        project=project)

def http_methods_disable(*methods):
    def decorator(cls):
        cls.http_method_names = [method for method in cls.http_method_names if method not in methods]
        return cls
    return decorator


@http_methods_disable('put', 'patch', 'delete')   
class CommentViewset(ModelViewSet):
    """View for Comment object. """
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated & IsContributor]  # Only for logged users
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        # queryset = Comment.objects.filter(active=True)
        queryset = Comment.objects.filter(issue=self.kwargs['issue_pk'])
        comment = self.request.GET.get('issue')
        if comment is not None:
            queryset = queryset.filter(id=comment)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user=self.request.user)


class UpdateDestroyCommentViewset(generics.RetrieveUpdateDestroyAPIView):
    """View for Comment object. """
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]  # Only for logged users
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        # queryset = Comment.objects.filter(active=True)
        queryset = Comment.objects.filter(issue=self.kwargs['issue_pk'])
        comment = self.request.GET.get('comment')
        if comment is not None:
            queryset = queryset.filter(id=comment)
        return queryset
    # fonction update et delete pour l'auteur du commentaire

# permissions sur les accès modification etc
# owasp

#Comment :
#   retirer liste vide et mettre status 404 si liste vide dans endpoint 
#   mettre l'url users ver authentication au lieu d'issue_tracking_system
#   ne pas ajouter le contributeur au projet si il est déjà présent 
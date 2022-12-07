from issue_tracking_system.models import Project, Contributor, Issue, Comment
from issue_tracking_system.serializers import ProjectSerializer, ContributorSerializer, IssueListSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status, generics

class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


# permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author_user_id == request.user


class ProjectViewset(ModelViewSet):

    permission_classes = [IsAuthenticated | IsOwnerOrReadOnly]  # Only for logged users and owner or only read
    serializer_class = ProjectSerializer

    # !!!! TODo Make condition for only admin get access to CRUD !!!!
    def get_queryset(self):
        queryset = Project.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user_id=self.request.user)

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE']:
    #         return [permissions.IsAdminUser()]
    #     return [permissions.IsAuthenticated()]

class ContributorViewset(ModelViewSet):

    # permission_classes = [IsAuthenticated]  # Only for logged users
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = Contributor.objects.all()
        contributor_id = self.request.GET.get('contributor_id')
        if contributor_id is not None :
            queryset = queryset.filter(contributor_id=contributor_id)
        return queryset
    

# class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    # permission_classes = [IsAuthenticated]  # Only for logged users
    # serializer_class = IssueListSerializer
    # detail_serializer_class = IssueDetailSerializer

    # def get_queryset(self):
    #     return Issue.objects.filter(active=True)

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return self.detail_serializer_class
    #     return super().get_serializer_class()

    # @action(detail=True, methods=['post'])
    # def disable(self, request, pk):
    #     self.get_object().disable()
    #     return Response()
class IssueViewset(ModelViewSet):

    serializer_class = IssueListSerializer

    def get_queryset(self):
        queryset = Issue.objects.filter(active=True)
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id__id=project_id)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user_id=self.request.user)

class CommentViewset(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]  # Only for logged users
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(active=True)
        comment_id = self.request.GET.get('comment_id')
        if comment_id is not None:
            queryset = queryset.filter(comment_id=comment_id)
        return queryset

# Create
# POST : Création d’une ressource.

# Read
# GET : Récupération d’une ressource ou d’une collection.

# Update
# PATCH : Modification d’une ressource ou d’une collection.

# PUT : Remplacement d’une ressource ou d’une collection.

# Delete
# DELETE : Suppression d’une ressource ou d’une collection.

# faire comments
# put patch del dans issue et comments
# permissions sur les acces modification etc
# faire api/users pour avoir tous les utilisateurs
# owasp

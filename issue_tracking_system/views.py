from issue_tracking_system.models import Project, Contributor, Issue, Comment
from issue_tracking_system.serializers import ProjectSerializer, ContributorSerializer, IssueListSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
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
        return obj.author_user == request.user


class ProjectViewset(ModelViewSet):
    """View for Project object. """

    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]  # Only for logged users and owner or only read
    serializer_class = ProjectSerializer
    detail_serializer_class =  ContributorSerializer

    # !!!! TODo Make condition for only admin get access to CRUD !!!!
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

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE']:
    #         return [permissions.IsAdminUser()]
    #     return [permissions.IsAuthenticated()]

# class ContributorViewset(ModelViewSet):
#     """View for Contributor object. """

#     # permission_classes = [IsAuthenticated]  # Only for logged users
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     serializer_class = ContributorSerializer

#     def get_queryset(self):
#         """Define the Query String usable in url."""
#         queryset = Contributor.objects.all()
#         contributor_id = self.request.GET.get('contributor_id')
#         if contributor_id is not None :
#             queryset = queryset.filter(contributor_id=contributor_id)
#         return queryset
    
class ContributorViewset(ModelViewSet):
    """View for Contributor object. """

    # permission_classes = [IsAuthenticated]  # Only for logged users
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Contributor.objects.all()
        contributor = self.request.GET.get('contributor')
        if contributor is not None :
            queryset = queryset.filter(id=contributor)
        return queryset

# class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

#     permission_classes = [IsAuthenticated]  # Only for logged users
#     serializer_class = ContributorListSerializer
#     detail_serializer_class =  ContributorDetailSerializer
#     def get_queryset(self):
#         return Issue.objects.filter(active=True)

#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return self.detail_serializer_class
#         return super().get_serializer_class()

#     @action(detail=True, methods=['post'])
#     def disable(self, request, pk):
#         self.get_object().disable()
#         return Response()


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
    """View for Issue object. """

    permission_classes = [IsAuthenticated] 
    serializer_class = IssueListSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Issue.objects.filter(active=True)
        project = self.request.GET.get('project')
        if project is not None:
            queryset = queryset.filter(project__id=project)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user=self.request.user)

class CommentViewset(ModelViewSet):
    """View for Comment object. """
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]  # Only for logged users
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Comment.objects.filter(active=True)
        comment = self.request.GET.get('comment')
        if comment is not None:
            queryset = queryset.filter(id=comment)
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the project
        serializer.save(author_user=self.request.user)


# permissions sur les accès modification etc
# modifier les _id du modèle
# owasp

from issue_tracking_system.models import Project, Contributor, Issue, Comment
from issue_tracking_system.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from issue_tracking_system.permissions import IsOwnerOrReadOnly, IsContributor


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
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """Define the Query String usable in url."""
        queryset = Contributor.objects.filter(
            project=self.kwargs['project_pk'])   
        # to return user instead of contributors
        # users_ids = contributor_queryset.values_list('user', flat=True)
        # queryset = User.objects.filter(pk__in=users_ids).all()
        return queryset

    def perform_create(self, serializer):
        # save the request.user as author when creating the issue
        project= Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(project=project)
    

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
        # save the request.user as author and the project_id in url 
        # when creating the issue
        project= Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.save(author_user=self.request.user,
                        project=project)


class CommentViewset(ModelViewSet):
    """View for Comment object. """
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
        # save the request.user as author when creating the comment
        issue= Issue.objects.get(pk=self.kwargs['issue_pk'])
        serializer.save(author_user=self.request.user, issue=issue)

    # fonction update et delete pour l'auteur du commentaire

# permissions sur les accès modification etc
# owasp

#Comment :
#   mettre l'url users ver authentication au lieu d'issue_tracking_system
#   ne pas ajouter le contributeur au projet si il est déjà présent 
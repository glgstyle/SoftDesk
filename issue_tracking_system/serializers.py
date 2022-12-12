from rest_framework import serializers
from rest_framework.serializers  import HyperlinkedIdentityField, HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from issue_tracking_system.models import Project, Contributor, Issue, Comment


class ProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'active', 'author']

    def validate_title(self, value):
        # Nous vérifions que le projet existe
        if Project.objects.filter(title=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Project already exists')
        return value


class ContributorSerializer(NestedHyperlinkedModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']


class IssueListSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'project_pk': 'project_id',
    }
    extra_kwargs = {
        'url': {'view_name': 'project', 'lookup_field':  
                'project-detail'},
    }
    # comment = CommentSerializer()
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'created_time', 'tag', 'priority', 'project', 'status', 'active', 'assignee_user', 'author']
    
    
# class CommentSerializer(serializers.ModelSerializer):
class CommentSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'issue_pk': 'issue_id',
        'project_pk': 'issue_project_id',
    }
    extra_kwargs = {
            'url': {'view_name': 'issues', 'lookup_field':  
                    'issue-detail'},
        }
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'active', 'issue', 'created_time']


# class ContributorListSerializer(serializers.ListSerializer):

#     class Meta:
#         model = Contributor
#         fields = ['id', 'user', 'project', 'permission', 'role']

# class ContributorDetailSerializer(serializers.Serializer):

#     project = serializers.SerializerMethodField()

#     class Meta:
#         model = Contributor
#         # fields = ['id', 'user', 'project', 'permission', 'role']
#         fields = ['user']


# class IssueListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Issue
#         fields = ['id', 'title', 'desc', 'project_id', 'created_time']

# class IssueDetailSerializer(serializers.ModelSerializer):

#     project = serializers.SerializerMethodField()

#     class Meta:
#         model = Issue
#         fields = ['id', 'title', 'desc', 'created_time', 'tag', 'priority', 'project_id', 'status', 'author_user', 'assignee_user']


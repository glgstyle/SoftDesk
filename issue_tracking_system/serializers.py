from rest_framework import serializers
from rest_framework.serializers  import HyperlinkedModelSerializer
from issue_tracking_system.models import Project, Contributor, Issue, Comment
from authentication.serializers import UsersSerializer


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


class ContributorSerializer(serializers.ModelSerializer):
    # will return the users info from object user
    user_object = UsersSerializer(source='user', many=False, read_only=True)
    
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role', 'user_object']
        read_only_fields = ['project']


class CommentSerializer(serializers.ModelSerializer):
    # will return the users info from object user
    user_object = UsersSerializer(source='author_user', many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user','user_object', 'active', 'issue', 'created_time']
        read_only_fields = ['issue', 'author_user']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'created_time', 'tag', 'priority', 'project', 'status', 'active', 'assignee_user', 'author']
        read_only_fields = ['project']

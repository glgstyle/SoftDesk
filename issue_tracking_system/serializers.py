from rest_framework import serializers
from rest_framework.serializers  import HyperlinkedIdentityField, HyperlinkedModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from issue_tracking_system.models import Project, Contributor, Issue, Comment
from authentication.models import User

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

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'active', 'issue', 'created_time']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'created_time', 'tag', 'priority', 'project', 'status', 'active', 'assignee_user', 'author']

from rest_framework import serializers

from issue_tracking_system.models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'active', 'author_user_id']

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


class IssueListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'created_time']

class IssueDetailSerializer(serializers.ModelSerializer):

    project = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'created_time', 'tag', 'priority', 'project', 'status', 'author_user', 'assignee_user']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['description', 'author_user_id', 'issue_id', 'created_time']
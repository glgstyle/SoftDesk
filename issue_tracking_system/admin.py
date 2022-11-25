from django.contrib import admin
from issue_tracking_system.models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display: ('id')


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display: ('id')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display: ('id')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: ('id')
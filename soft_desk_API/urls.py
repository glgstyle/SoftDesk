from django.contrib import admin
from django.urls import include, path
from issue_tracking_system.views import (
    ProjectViewset, ContributorViewset, IssueViewset, CommentViewset)
from authentication.views import UsersViewset
from rest_framework_nested import routers


# project
router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='project')

# contributors
contributors_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
contributors_router.register(
    r'users', ContributorViewset, basename='project-users')

# issues
issues_router = routers.NestedSimpleRouter(
    router, r'projects', lookup='project')
issues_router.register(
    r'issues', IssueViewset, basename='project-issues')

# comments
comments_router = routers.NestedSimpleRouter(
    issues_router, 'issues', lookup='issue')
comments_router.register(
    'comments', CommentViewset, basename='project-issues-comments')

# users
router.register('users', UsersViewset, basename='users')
router.register('comment', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"api/", include("authentication.urls")),
    path(r'api/', include(router.urls)),
    path(r'api/', include(contributors_router.urls)),
    path(r'api/', include(issues_router.urls)),
    path(r'api/', include(comments_router.urls)),
]

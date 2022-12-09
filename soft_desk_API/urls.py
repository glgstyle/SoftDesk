from django.contrib import admin
from django.urls import include, path
from issue_tracking_system.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset
from rest_framework import routers
from authentication.views import UsersViewset

from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'users', ContributorViewset, basename='contributors')
projects_router.register(r'issues', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')
router.register('users', UsersViewset, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),
    path('api/', include(router.urls)),
    path(r'api/', include(projects_router.urls)),
]

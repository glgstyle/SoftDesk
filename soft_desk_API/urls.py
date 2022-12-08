from django.contrib import admin
from django.urls import include, path
from issue_tracking_system.views import ProjectViewset, ContributorViewset, IssueViewset, CommentViewset
from authentication.views import UserViewset, UserRegistrationView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('user', UserViewset, basename='user')
router.register('projects', ProjectViewset, basename='project')
router.register('contributor', ContributorViewset, basename='contributor')
# router.register('projects/{id}/users', ContributorViewset, basename='contributor')
router.register('issue', IssueViewset, basename='issue')
router.register('comment', CommentViewset, basename='comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),
    path('api/', include(router.urls)),
]

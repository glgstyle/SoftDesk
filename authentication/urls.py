
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from authentication.views import UserRegistrationView


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]

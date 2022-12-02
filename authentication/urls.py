
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from authentication.views import UserRegistrationView


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', TokenBlacklistView.as_view(), name='logout'),

]

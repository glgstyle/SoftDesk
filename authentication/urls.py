
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import EmailTokenObtainPairView, UserRegistrationView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('register/', UserRegistrationView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),

]

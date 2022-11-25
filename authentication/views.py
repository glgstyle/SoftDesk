# from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer
# Create your views here.

class UserViewset(ReadOnlyModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter()
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset
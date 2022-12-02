from rest_framework.viewsets import ReadOnlyModelViewSet
from authentication.models import User
from authentication.serializers import RegistrationSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.response import Response
from authentication.serializers import RegistrationSerializer


class UserViewset(ReadOnlyModelViewSet):

    serializer_class = RegistrationSerializer

    def get_queryset(self):
        queryset = User.objects.filter()
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class UserRegistrationView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

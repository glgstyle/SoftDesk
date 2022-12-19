from rest_framework.viewsets import ReadOnlyModelViewSet
from authentication.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from authentication.serializers import RegistrationSerializer, UsersSerializer


class UserRegistrationView(generics.CreateAPIView):
    """View to register a User. """

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewset(ReadOnlyModelViewSet):
    """View to list all users. """

    serializer_class = UsersSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

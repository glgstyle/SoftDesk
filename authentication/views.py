# from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import UserSerializer, TokenObtainPairSerializer

class UserViewset(ReadOnlyModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter()
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class UserRegistrationView(generics.CreateAPIView):
    
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    serializer_class = UserSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response(user_data,status=status.HTTP_201_CREATED)

# class UserRegistrationView(APIView):
    
#     permission_classes = [AllowAny]
#     http_method_names = ['post']

#     def post(self, *args, **kwargs):
#         serializer = UserSerializer(data=self.request.data)
#         if serializer.is_valid():
#             get_user_model().objects.create_user(**serializer.validated_data)
#             return Response(status=HTTP_201_CREATED)
#         return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
from django.db import IntegrityError
from rest_framework import serializers
# from django.contrib import messages
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']

    # def validate_username(self, value):
    #     if User.objects.filter(username=value).exists():
    #         raise serializers.ValidationError('Email already exists')
    #     return value

    def create(self, validated_data):
        """ Create and return a new `User` instance,
            given the validated data. """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.email = user.username
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    
    # def update(self, user, validated_data):
    #     """
    #     Update and return an existing `User` instance, given the validated data.
    #     """
    #     user.email = validated_data.get('email', user.email)
    #     user.username = validated_data.get('email', user.email)
    #     user.password = validated_data.get('password', user.password)
    #     user.first_name = validated_data.get('first_name', user.first_name)
    #     user.last_name = validated_data.get('last_name', user.last_name)
    #     user.save()
    #     return user

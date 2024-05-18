from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers, status
from .models import UserComplaint


class UserComplaintSerializer(ModelSerializer):
    class Meta:
        model = UserComplaint
        fields = ('text',)


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_joined')



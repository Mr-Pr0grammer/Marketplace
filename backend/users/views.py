from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserComplaint
from .serializers import UserComplaintSerializer, UserProfileSerializer


class UserComplaintAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserComplaintSerializer(data=request.data)
        if serializer.is_valid():
            UserComplaint.objects.create(
                user=request.user,
                text=request.data['text']
            )
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)


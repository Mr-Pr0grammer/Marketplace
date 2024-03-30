from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserComplaint
from .serializers import UserComplaintSerializer


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
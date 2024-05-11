from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
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


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             token.
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(data={f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


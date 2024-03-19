from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        return Response({'cerrect': 'correeccet'}, status=status.HTTP_200_OK)



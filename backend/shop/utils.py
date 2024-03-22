from .models import Product
from rest_framework.response import Response
from rest_framework import status


def product_exists(request):
    try:
        product = Product.objects.get(id=request.data['product'])
        return product
    except Product.DoesNotExist:
        return Response(data='No such product', status=status.HTTP_404_NOT_FOUND)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import Category, Product, ProductCartItem, ProductCart
from .serializers import ProductSerializer, CategorySerializer, ProductCartItemSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404


class ProductsList(ListAPIView):
    queryset = Product.objects.filter(active='Active').order_by('-updated')
    serializer_class = ProductSerializer


class CategoriesList(ListAPIView):
    queryset = Category.objects.order_by('-updated')
    serializer_class = CategorySerializer


class GetProduct(RetrieveAPIView):
    queryset = Product.objects.filter(active='Active').order_by('-updated')
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductCartItemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ProductCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart = ProductCart.objects.get(user=request.user)
            try:
                product = Product.objects.get(id=request.data['product'])
            except Http404:
                return Response(data='No such product', status=status.HTTP_404_NOT_FOUND)
            try:
                cart_item = ProductCartItem.objects.get(product=product, cart=cart)
                cart_item.quantity = request.data['quantity']
                cart_item.save()
                return Response(data='Product quantity was updated', status=status.HTTP_202_ACCEPTED)
            except Http404:
                ProductCartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=serializer.data['quantity']
                )
            return Response(data='Product has been added', status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

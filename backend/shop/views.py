from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils import product_exists
from .models import Category, Product, ProductCartItem, ProductCart
from .serializers import ProductSerializer, CategorySerializer, ProductCartItemSerializer


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

    def get(self, request):
        cart = ProductCart.objects.get(user=request.user)
        cart_items = Product.objects.filter(cart_items__cart=cart).all()
        serializer = ProductSerializer(cart_items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart = ProductCart.objects.get(user=request.user)
            product = product_exists(request)
            if 'quantity' not in request.data:
                quantity = 1
            else:
                quantity = request.data['quantity']
            try:
                cart_item = ProductCartItem.objects.get(product=product, cart=cart)
                if quantity > product.quantity:
                    return Response(data='Exceeded quantity available', status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity = quantity
                cart_item.save()
                return Response(data='Product quantity was updated', status=status.HTTP_202_ACCEPTED)
            except ProductCartItem.DoesNotExist:
                if quantity > product.quantity:
                    return Response(data='Exceeded quantity available', status=status.HTTP_400_BAD_REQUEST)
                ProductCartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=quantity
                )
            return Response(data='Product has been added', status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = ProductCart.objects.get(user=request.user)
        serializer = ProductCartItemSerializer(data=request.data)

        if serializer.is_valid():
            product = product_exists(request)
            try:
                cart_item = ProductCartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
                return Response(data='Product has been removed', status=status.HTTP_200_OK)
            except ProductCartItem.DoesNotExist:
                return Response(data='No such product', status=status.HTTP_404_NOT_FOUND)

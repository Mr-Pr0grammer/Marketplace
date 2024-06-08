from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .utils import product_exists
from .models import (
    Category, Product,
    ProductCartItem, ProductCart,
    ProductComment
)
from .serializers import (
    ProductSerializer, ProductAddSerializer,
    CategorySerializer, ProductCartItemSerializer,
    ProductCommentSerializer
)



class ProductsListFilterView(ListAPIView):
    queryset = Product.objects.filter(active='Active').all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('category_id',)
    ordering_fields = ('price', 'name')
    search_fields = ('name',)



class ProductsListByOwner(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user).order_by('-created')


class CategoriesList(ListAPIView):
    queryset = Category.objects.order_by('-updated')
    serializer_class = CategorySerializer
    # filter_backends = None


class GetProduct(RetrieveAPIView):
    queryset = Product.objects.filter(active='Active').order_by('-updated')
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductCartItemAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = ProductCart.objects.get(user=request.user)
        cart_items = Product.objects.filter(cart_items__cart=cart).all()
        serializer = ProductSerializer(cart_items, many=True, context={'request': request})
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

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
                    return Response(data='Exceeded quantity available',
                                    status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity = quantity
                cart_item.save()
                return Response(data='Product quantity was updated',
                                status=status.HTTP_202_ACCEPTED)
            except ProductCartItem.DoesNotExist:
                if quantity > product.quantity:
                    return Response(data='Exceeded quantity available',
                                    status=status.HTTP_400_BAD_REQUEST)
                ProductCartItem.objects.create(
                    product=product,
                    cart=cart,
                    quantity=quantity
                )
            return Response(data='Product has been added',
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = ProductCart.objects.get(user=request.user)
        serializer = ProductCartItemSerializer(data=request.data)

        if serializer.is_valid():
            product = product_exists(request)
            try:
                cart_item = ProductCartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
                return Response(data='Product has been removed',
                                status=status.HTTP_200_OK)
            except ProductCartItem.DoesNotExist:
                return Response(data='No such product',
                                status=status.HTTP_404_NOT_FOUND)


class DeleteCartItemsAll(APIView):
    def delete(self, request):
        cart = ProductCart.objects.get(user=request.user)
        cart_items = ProductCartItem.objects.filter(cart=cart)
        cart_items.delete()
        return Response(data='All items have been deleted!',
                        status=status.HTTP_200_OK)


class AddProductView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['POST']

    def post(self, request):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ProductCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            slug = kwargs.get('slug')
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comments = ProductComment.objects.filter(product__slug=slug)
        count = comments.count()
        serializer = ProductCommentSerializer(comments, many=True, context={'request': request})
        return Response(status=status.HTTP_200_OK,
                        data=[{'count': count}, serializer.data])

    def post(self, request):
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


















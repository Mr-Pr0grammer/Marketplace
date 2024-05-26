from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils import product_exists
from .models import Category, Product, ProductCartItem, ProductCart
from .serializers import ProductSerializer, CategorySerializer, ProductCartItemSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.filter(active='Active').order_by('-updated')
    serializer_class = ProductSerializer


class ProductsListByCategory(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.kwargs.get('slug')
        return Product.objects.filter(active='Active', category__slug=category).order_by('-updated')


class ProductsListByPrice(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        price = self.kwargs.get('str')
        if price == 'upper':
            return Product.objects.order_by('-price')
        elif price == 'lower':
            return Product.objects.order_by('price')


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
        serializer = ProductSerializer(cart_items, many=True, context={'request': request})
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


class DeleteCartItemsAll(APIView):
    def delete(self, request):
        cart = ProductCart.objects.get(user=request.user)
        cart_items = ProductCartItem.objects.filter(cart=cart)
        cart_items.delete()
        return Response(data='All items have been deleted!', status=status.HTTP_200_OK)


class AddProductView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # data = request.data.copy()  # Make a mutable copy of request data
        # category_id = request.data.get('category')
        #
        # if not category_id:
        #     return Response({'error': 'No category ID provided'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # try:
        #     category = Category.objects.get(id=category_id)
        # except Category.DoesNotExist:
        #     return Response({'error': 'Invalid category ID provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the full category data to the request data
        # data['category'] = {
        #     'id': category.id,
        #     'name': category.name,
        #     'title': category.title,
        #     'description': category.description,
        #     'slug': category.slug,
        #     'image': category.image.url if category.image else None,
        #     'created': category.created.isoformat(),
        #     'updated': category.updated.isoformat()
        # }

        serializer = ProductSerializer(data=request.data)
        serializer.o
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # category = Category.objects.get(slug=request.data['slug'])
        # Product.objects.create(
        #     owner=request.user,
        #     category=category,
        #     discount=request.data['discount'],
        #     image=request.data['image'],
        #     name=request.data['name'],
        #     slug=request.data['slug'],
        #     price=request.data['price'],
        #     quantity=request.data['quantity'],
        #     short_description=request.data['short_description'],
        #     long_description=request.data['long_description'],
        #     active=request.data['active']
        # )















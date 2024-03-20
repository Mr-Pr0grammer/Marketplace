from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated


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

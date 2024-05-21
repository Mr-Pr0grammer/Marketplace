from .models import Category, Product, ProductCartItem
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ('id', 'name', 'slug', 'get_image', 'created', 'updated')
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        # fields = ('id', 'image', 'active', 'category', 'name', 'quantity', 'price', 'slug', 'short_description', 'long_description', 'get_image')
        fields = '__all__'


class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCartItem
        fields = ('product', 'quantity')
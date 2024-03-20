from .models import Category, Product
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'get_image', 'created', 'updated')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'price', 'slug', 'short_description', 'long_description', 'get_image')
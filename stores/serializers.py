from rest_framework import serializers
from . models import Category,Products

# CATEGORY SERIALIZERS
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# PRODUCT SERIALIZERS
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

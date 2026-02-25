from rest_framework import serializers
from . models import *

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

# CART SERIALIZERS
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

# CART SERIALIZERS
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'

# CART SERIALIZERS
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# CART SERIALIZERS
class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['cart','amount','subtotal','ref','order_status','payment_completed']

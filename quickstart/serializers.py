from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def create(self, Validate_data):
        user = User.objects.create_user(
            username=Validate_data['username'],
            email = Validate_data['email'],
            password=  Validate_data['password'],
        )
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields ='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields= '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    Product= ProductSerializer(read_only =True)
    class Meta:
        model = CartItem
        fields= '__all__'

class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model= CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= order
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    Product= ProductSerializer(read_only =True)
    class Meta:
        model= OrderItem
        fields = '__all__'









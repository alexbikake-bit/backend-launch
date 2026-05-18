# from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny

# Create your views here.

# register user
@api_view(['POST'])

def register_user(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save
        return Response(serializer.data)
    
    return Response(serializer.errors)

# GET ALL PRODUCTS
@api_view (['GET'])
def get_products(request):
    products = Product.objects.all()

    search = request.GET.get('search')

    if search:
        products = products.filter(name_icontains= search)

    serializer= ProductSerializer(products, many=True)
    return Response(serializer.data)

# GET SINGLE PRODUCT

@api_view(['GET'])
def get_product(request,pk):
     product = Product.objects.get(id=pk)
     serializer = ProductSerializer(product)
     return Response(serializer.data)

# CREATE PRODUCT
@api_view(['POST'])
@permission_classes([IsAdminUser])

def create_product(request):
    serializer = ProductCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)

# UPDATE PRODUCT
@api_view(['PUT'])
@permission_classes([IsAdminUser])

def update_product(request,pk):
    product =Product.objects.get(id=pk)
    serializer = ProductCreateSerializer(product, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)

# DELETE
@api_view(['DELETE'])
@permission_classes([IsAdminUser])

def delete_product(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()

    return Response('Product deleted')

# GET CATEGORIES
@api_view(['GET'])
def get_category(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# CREATE CATEGORY
@api_view(['POST'])
@permission_classes([AllowAny])

def create_category(request):
    serializer = CategorySerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)

# CREATE CART
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def create_cart(request):
    cart = cart.objects.create(user=request.user)
    serializer = CartSerializer(cart)
    return Response (serializer.data)

# ADD TO CART
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_to_cart(request):
    serializer = CartItemCreateSerializer(data= request.data)
   
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response (serializer.errors)

# GET CART ITEM
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_cart_item(request):
    items = CartItem.objects.filter(cart_user=request.user)
    serializer = CartItemSerializer(items, many=True)
    return Response(serializer.data)
   
# CREATE ORDER
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def create_order(request):
    cart_items = CartItem.objects.filter(cart_user=request.user)

    total = 0
    
    for item in cart_items:
        total += item.product.price * item.quantity

    order = order.objects.create(
        user = request.user,
        total_price = total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order =order,
            product = item.product,
            quantity = item.quantity
        )

    cart_items.delete()

    serializer = OrderSerializer(order)
    return Response(serializer.data)

# GET ORDERS
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def get_orders(request):
    orders = order.objects.filter(user= request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
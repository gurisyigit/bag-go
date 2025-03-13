from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt


from django.utils import timezone
from django.shortcuts import redirect, render

from rest_framework import filters, generics, status, viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers

from bs4 import BeautifulSoup
import requests
import logging

import json
import io
import random
import os

from .models import AuthToken, UserProfile, ProductCategory, Product, Bag, Order, LikedProduct
from .serializer import UserSerializer, UserProfileSerializer, RegisterSerializer, LoginSerializer, ProductCategorySerializer, ProductSerializer, BagSerializer, OrderSerializer
from django.http import FileResponse
from django.conf import settings
from django.urls import path

 
@api_view(['POST'])
@permission_classes([AllowAny])  # Allows any user to access this endpoint
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        try:
            Token.objects.get(user=user).delete()
        except Exception:
            pass
        drf_token = Token.objects.create(user=user)
        token = AuthToken.objects.create(user=user, token=drf_token.key)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.token
            }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
   

@api_view(['POST'])
@permission_classes([AllowAny])  # Allows any user to access this endpoint
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    firstname = request.data.get('first_name')
    lastname = request.data.get('last_name')
    address = request.data.get('address')
    tc = request.data.get('tc')
    birth_year = request.data.get('birth_year')


    # Validate input data
    if not username or not email or not password or not firstname or not lastname or not address or not tc or not birth_year:
        return Response(
            {'error': 'All fields are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username or email is already taken
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new user
    user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
    
    drf_token = Token.objects.create(user=user)
    token = AuthToken.objects.create(token=drf_token.key, user=user)
    try:
        new_profile = UserProfile.objects.create(user=user, address=address, tc=tc, birth_year=birth_year, balance=0)
        new_profile.save()
    except Exception as e:
        user.delete()
        return Response({'error': 'Failed to create user profile.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # T.C. identity verification request
    # body = f"""<?xml version="1.0" encoding="UTF-8"?>
    # <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    # <soap:Body>
    #     <TCKimlikNoDogrula xmlns="http://tckimlik.nvi.gov.tr/WS">
    #     <TCKimlikNo>{int(tc)}</TCKimlikNo>
    #     <Ad>{str(firstname)}</Ad>
    #     <Soyad>{str(lastname)}</Soyad>
    #     <DogumYili>{int(birth_year)}</DogumYili>
    #     </TCKimlikNoDogrula>
    # </soap:Body>
    # </soap:Envelope>"""

    # headers = {
    #     'content-type': 'text/xml; charset=UTF-8',
    #     'host': 'tckimlik.nvi.gov.tr',
    # }

    # try:
    #     r = requests.post(
    #         "https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL",
    #         headers=headers, data=body.encode('utf-8')
    #     )
    #     xml = BeautifulSoup(r.content, 'xml')
    #     result = xml.find('soap:Body').text

    #     if result != "true":
    #         user.delete()
    #         return Response({"error": "Invalid TC number or user data"}, status=status.HTTP_400_BAD_REQUEST)

    # except Exception as e:
    #     user.delete()
    #     return Response({'error': 'Failed to verify TC number.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "user": UserSerializer(user).data,
        "token": token.token
        }, status=status.HTTP_201_CREATED)

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategory.objects.all().order_by('id')
    serializer_class = ProductCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    filter_fields = ['id', 'name']

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name', 'category__name', 'price', 'old_price', 'is_discounted', 'stock', 'barcode']
    ordering_fields = ['id', 'name', 'category', 'price', 'old_price', 'is_discounted', 'stock', 'barcode']
    filter_fields = ['id', 'name', 'category', 'price', 'old_price', 'is_discounted', 'stock', 'barcode']

    @action(detail=False, methods=['get'], url_path='product_images/(?P<filename>[^/]+)')
    def image(self, request, filename=None):
        file_path = os.path.join(settings.MEDIA_ROOT, 'product_images', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
        else:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        

#View Cart
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def view_cart(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = AuthToken.objects.get(token=token).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cart_items = Bag.objects.filter(user=user)
        serializer = BagSerializer(cart_items, many=True)
        if not cart_items:
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Bag.DoesNotExist:
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_404_NOT_FOUND)
    

#Add to Cart
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    user = request.data.get('token')

    if not product_id:
        return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not quantity:
        return Response({'error': 'Quantity is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if product.stock < quantity:
        return Response({'error': 'Not enough stock.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_item = Bag.objects.get(user=user, product=product)
        if cart_item.product.stock < cart_item.quantity + quantity:
            return Response({'error': 'Not enough stock.'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity += quantity
        cart_item.save()
    except Bag.DoesNotExist:
        cart_item = Bag.objects.create(user=user, product=product, quantity=quantity)

    return Response({'message': 'Product added to cart successfully.'}, status=status.HTTP_200_OK)

    
#Checkout
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    user = request.data.get('token')
    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_items = Bag.objects.filter(user=user)
    if not cart_items:
        return Response({'error': 'Cart is empty.'}, status=status.HTTP_404_NOT_FOUND)
    
    total_price = 0
    for cart_item in cart_items:
        total_price += cart_item.product.price * cart_item.quantity

    user_profile = UserProfile.objects.get(user=user)

    if user_profile.balance < total_price:
        return Response({'error': 'Not enough balance.'}, status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.create(user=user, total_price=total_price)
    for cart_item in cart_items:
        order.products.add(cart_item.product)
        cart_item.product.stock -= cart_item.quantity
        cart_item.delete()
    
    user_profile.balance -= total_price
    user_profile.save()

    order_serialized = OrderSerializer(order).data
    
    return Response({'message': 'Order placed successfully.', 'order': order_serialized}, status=status.HTTP_200_OK)


# Serializer for updating user profile details
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Basic fields; add more if needed
        extra_kwargs = {'username': {'required': False}, 'email': {'required': False}}

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# View for updating profile details
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for updating password
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_password(request):
    serializer = UpdatePasswordSerializer(data=request.data)
    
    if serializer.is_valid():
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not request.user.check_password(old_password):
            return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.set_password(new_password)
        request.user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = AuthToken.objects.get(token=token).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        Token.objects.get(user=user).delete()
    except Exception:
        pass
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_liked_products(request):
    user = request.data.get('token')
    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    liked_products = LikedProduct.objects.filter(user=user)
    if not liked_products:
        return Response({'error': 'No liked products found.'}, status=status.HTTP_404_NOT_FOUND)
    
    products = [liked_product.product for liked_product in liked_products]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_product(request):
    product_id = request.data.get('product_id')
    user = request.data.get('token')

    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

    if not product_id:
        return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if LikedProduct.objects.filter(user=user, product=product).exists():
        LikedProduct.objects.filter(user=user, product=product).delete()
        return Response({'message': 'Product unliked successfully.'}, status=status.HTTP_200_OK)
    

    LikedProduct.objects.create(user=user, product=product)
    return Response({'message': 'Product liked successfully.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_orders(request):
    user = request.data.get('token')
    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    orders = Order.objects.filter(user=user)
    if not orders:
        return Response({'error': 'No orders found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_order_confirmation(request):
    confirmation_code = request.data.get('code')
    user = request.data.get('token')

    if not user:
        return Response({'error': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = AuthToken.objects.get(token=user).user
    except AuthToken.DoesNotExist:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

    user_admin = user.is_superuser

    if not user_admin:
        return Response({'error': 'You are not authorized to access this endpoint.'}, status=status.HTTP_401_UNAUTHORIZED)

    if not confirmation_code:
        return Response({'error': 'Confirmation code is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(confirmation_code=confirmation_code)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
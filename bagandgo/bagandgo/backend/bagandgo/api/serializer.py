from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import UserProfile, ProductCategory, Product, Bag, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ["username", 'id']
        extra_kwargs = {
            'email': {'write_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = serializers.CharField(write_only=True, required=False)
    balance = serializers.FloatField(read_only=True, required=False)
    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'balance']
        read_only_fields = ['user', 'balance']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_id', 'price', 'old_price', 'is_discounted', 'image', 'stock', 'barcode']

class BagSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Bag
        fields = ['id', 'user', 'product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'confirmation_code', 'created_at']
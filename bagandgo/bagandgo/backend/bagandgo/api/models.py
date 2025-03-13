from django.db import models
from rest_framework.authtoken.models import Token
import random


# Create your models here.

class AuthToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.token} - {self.user.username}"

class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tc = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    birth_year = models.IntegerField(null=True, blank=True)
    balance = models.FloatField(default=0)
    
    def __str__(self):
        return self.user.username

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.FloatField()
    old_price = models.FloatField(default=0)
    is_discounted = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/')
    stock = models.IntegerField()
    barcode = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Bag(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.FloatField()
    confirmation_code = models.CharField(max_length=255, default=random.randint(100000, 999999))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.confirmation_code}"

class LikedProduct(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
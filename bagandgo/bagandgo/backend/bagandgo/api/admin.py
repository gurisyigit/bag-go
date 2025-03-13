from django.contrib import admin
from .models import AuthToken, UserProfile, ProductCategory, Product, Bag, Order, LikedProduct

admin.site.register(AuthToken)
admin.site.register(UserProfile)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Bag)
admin.site.register(Order)
admin.site.register(LikedProduct)
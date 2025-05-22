from django.contrib import admin
from stock.models import User
from core.models.product import Product, Category
from core.models.order import Order, OrderItem

# Register models for admin interface
# User model is already registered in stock app
# admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)

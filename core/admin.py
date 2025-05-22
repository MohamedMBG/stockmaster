from django.contrib import admin
from core.models.user import User
from core.models.product import Product, Category
from core.models.order import Order, OrderItem

# Register models for admin interface
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)

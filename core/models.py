# Import all models from the models package
# Using settings.AUTH_USER_MODEL instead of direct import
from django.conf import settings
from core.models.product import Product, Category
from core.models.order import Order, OrderItem

# This allows imports like: from core.models import User
# Instead of direct imports from specific modules
User = settings.AUTH_USER_MODEL

# Import all models from the models package
from core.models.user import User
from core.models.product import Product, Category
from core.models.order import Order, OrderItem

# This allows imports like: from core.models import User
# Instead of: from core.models.user import User

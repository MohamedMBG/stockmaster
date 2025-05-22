from django.db import models
from django.utils import timezone
from django.conf import settings
from core.models.product import Product

# Use the AUTH_USER_MODEL setting instead of direct import
User = settings.AUTH_USER_MODEL

class Order(models.Model):
    """Order model for tracking customer orders."""
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.client.username}"
    
    def get_items_count(self):
        """Get the total number of items in the order."""
        return self.items.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
    
    def get_status_display_class(self):
        """Get the CSS class for the status display."""
        status_classes = {
            'PENDING': 'warning',
            'APPROVED': 'primary',
            'SHIPPED': 'info',
            'DELIVERED': 'success',
            'CANCELLED': 'danger',
        }
        return status_classes.get(self.status, 'secondary')

class OrderItem(models.Model):
    """Order item model for tracking products in an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderitem')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_subtotal(self):
        """Calculate the subtotal for this item."""
        return self.quantity * self.unit_price

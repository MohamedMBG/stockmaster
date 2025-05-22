from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.core.paginator import Paginator

from core.models.product import Product, Category
from core.models.order import Order, OrderItem
from core.decorators import client_required

@login_required
@client_required
def client_dashboard(request):
    """
    Client dashboard view showing recent orders and featured products.
    """
    # Get client's recent orders
    recent_orders = Order.objects.filter(client=request.user).order_by('-created_at')[:5]
    
    # Get available products for featured display
    featured_products = Product.objects.filter(quantity__gt=0).order_by('?')[:4]
    
    # Get order statistics
    order_count = Order.objects.filter(client=request.user).count()
    pending_orders = Order.objects.filter(client=request.user, status='PENDING').count()
    
    context = {
        'recent_orders': recent_orders,
        'featured_products': featured_products,
        'order_count': order_count,
        'pending_orders': pending_orders,
    }
    
    return render(request, 'client/dashboard.html', context)

@login_required
@client_required
def client_catalog(request):
    """
    Product catalog view for clients to browse and order products.
    """
    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Base queryset
    products = Product.objects.filter(quantity__gt=0)
    
    # Apply filters
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Order by name
    products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all().order_by('name')
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    
    return render(request, 'client/catalog.html', context)

@login_required
@client_required
def client_add_to_cart(request):
    """
    Add a product to the shopping cart.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
            
            # Check if quantity is valid
            if quantity <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect('client_catalog')
            
            if quantity > product.quantity:
                messages.error(request, f"Sorry, only {product.quantity} units of {product.name} are available.")
                return redirect('client_catalog')
            
            # Initialize cart in session if it doesn't exist
            if 'cart' not in request.session:
                request.session['cart'] = {}
            
            # Add to cart
            cart = request.session['cart']
            product_key = str(product_id)
            
            if product_key in cart:
                # Update quantity if product already in cart
                cart[product_key]['quantity'] += quantity
            else:
                # Add new product to cart
                cart[product_key] = {
                    'quantity': quantity,
                    'price': float(product.unit_price),
                    'name': product.name
                }
            
            request.session.modified = True
            messages.success(request, f"{product.name} added to your cart.")
            
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
        
    return redirect('client_place_order')

@login_required
@client_required
def client_update_cart(request):
    """
    Update the quantity of a product in the cart.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if 'cart' in request.session and str(product_id) in request.session['cart']:
            # Check if quantity is valid
            if quantity <= 0:
                # Remove item if quantity is zero or negative
                del request.session['cart'][str(product_id)]
                messages.success(request, "Item removed from cart.")
            else:
                # Update quantity
                try:
                    product = Product.objects.get(id=product_id)
                    
                    if quantity > product.quantity:
                        messages.error(request, f"Sorry, only {product.quantity} units of {product.name} are available.")
                        quantity = product.quantity
                    
                    request.session['cart'][str(product_id)]['quantity'] = quantity
                    messages.success(request, "Cart updated.")
                    
                except Product.DoesNotExist:
                    messages.error(request, "Product not found.")
            
            request.session.modified = True
    
    return redirect('client_place_order')

@login_required
@client_required
def client_remove_from_cart(request):
    """
    Remove a product from the cart.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        if 'cart' in request.session and str(product_id) in request.session['cart']:
            del request.session['cart'][str(product_id)]
            request.session.modified = True
            messages.success(request, "Item removed from cart.")
    
    return redirect('client_place_order')

@login_required
@client_required
def client_place_order(request):
    """
    View for placing an order with items in the cart.
    """
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Prepare cart items for display
    cart_items = []
    cart_subtotal = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            subtotal = quantity * float(product.unit_price)
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            
            cart_subtotal += subtotal
            
        except Product.DoesNotExist:
            # Remove invalid products from cart
            del cart[product_id]
            request.session.modified = True
    
    # Calculate shipping and total
    shipping_cost = 10.00 if cart_subtotal > 0 else 0
    cart_total = cart_subtotal + shipping_cost
    
    context = {
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'shipping_cost': shipping_cost,
        'cart_total': cart_total,
    }
    
    return render(request, 'client/place_order.html', context)

@login_required
@client_required
def client_place_order_submit(request):
    """
    Process the order submission.
    """
    if request.method == 'POST':
        # Get cart from session
        cart = request.session.get('cart', {})
        
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('client_catalog')
        
        shipping_address = request.POST.get('shipping_address')
        notes = request.POST.get('notes', '')
        
        if not shipping_address:
            messages.error(request, "Shipping address is required.")
            return redirect('client_place_order')
        
        # Calculate total amount
        total_amount = 0
        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                quantity = item_data['quantity']
                
                # Verify product availability
                if quantity > product.quantity:
                    messages.error(request, f"Sorry, only {product.quantity} units of {product.name} are available.")
                    return redirect('client_place_order')
                
                total_amount += quantity * float(product.unit_price)
                
            except Product.DoesNotExist:
                # Remove invalid products from cart
                del cart[product_id]
                request.session.modified = True
        
        # Add shipping cost
        shipping_cost = 10.00
        total_amount += shipping_cost
        
        # Create order
        order = Order.objects.create(
            client=request.user,
            status='PENDING',
            total_amount=total_amount,
            shipping_address=shipping_address,
            notes=notes
        )
        
        # Create order items
        for product_id, item_data in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.unit_price
            )
            
            # Update product quantity
            product.quantity -= quantity
            product.save()
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f"Order #{order.id} placed successfully. Thank you for your purchase!")
        return redirect('client_orders')
    
    return redirect('client_place_order')

@login_required
@client_required
def client_orders(request):
    """
    View for displaying client's orders.
    """
    orders = Order.objects.filter(client=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'client/orders.html', context)

@login_required
@client_required
def client_order_detail(request, order_id):
    """
    View for displaying details of a specific order.
    """
    try:
        order = Order.objects.get(id=order_id, client=request.user)
        order_items = OrderItem.objects.filter(order=order).select_related('product')
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        
        return render(request, 'client/order_detail.html', context)
        
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('client_orders')

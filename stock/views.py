from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F
from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy
import csv
import datetime

from .models import User, Product, Category, Supplier, StockTransaction, Order, OrderItem, Alert, Message
from .forms import (
    LoginForm, ClientRegistrationForm, SupervisorCreationForm, UserProfileForm, 
    ProfileImageForm, ProductForm, CategoryForm, SupplierForm, StockTransactionForm
)

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'stock/login.html', {'form': form})

def register_view(request):
    # Only allow client registration
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully. Welcome, {user.username}!")
            return redirect('dashboard')
        else:
            # Add error message if form is invalid
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = ClientRegistrationForm()
    return render(request, 'stock/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Admin-only view for creating supervisor accounts
@login_required
def add_supervisor(request):
    # Check if user is admin
    if not request.user.is_admin():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SupervisorCreationForm(request.POST)
        if form.is_valid():
            supervisor = form.save()
            messages.success(request, f"Supervisor account for {supervisor.username} created successfully.")
            return redirect('user_list')
    else:
        form = SupervisorCreationForm()
    
    return render(request, 'stock/add_supervisor.html', {'form': form})

# Dashboard View
@login_required
def dashboard(request):
    # Common data for all users
    context = {
        'total_products': Product.objects.count(),
        'low_stock_count': Product.objects.filter(quantity__lte=models.F('reorder_level')).count(),
    }
    
    # Role-specific data
    if request.user.is_admin() or request.user.is_supervisor():
        # Admin and Supervisor see full dashboard
        context.update({
            'total_orders': Order.objects.count(),
            'total_suppliers': Supplier.objects.count(),
            'recent_transactions': StockTransaction.objects.select_related('product', 'created_by').order_by('-timestamp')[:10],
            
            # Data for charts
            'product_names': list(Product.objects.values_list('name', flat=True)[:10]),
            'product_quantities': list(Product.objects.values_list('quantity', flat=True)[:10]),
            'category_names': list(Category.objects.annotate(product_count=Count('product')).values_list('name', flat=True)),
            'category_counts': list(Category.objects.annotate(product_count=Count('product')).values_list('product_count', flat=True)),
        })
    elif request.user.is_client():
        # Client sees their orders and available products
        context.update({
            'total_orders': Order.objects.filter(client=request.user).count(),
            'recent_orders': Order.objects.filter(client=request.user).order_by('-created_at')[:5],
            'available_products': Product.objects.filter(quantity__gt=0)[:8],
        })
    elif request.user.is_supplier():
        # Supplier sees products they supply
        context.update({
            'supplied_products': Product.objects.filter(supplier__user=request.user),
            'recent_orders': Order.objects.filter(items__product__supplier__user=request.user).distinct().order_by('-created_at')[:5],
        })
    
    return render(request, 'stock/dashboard.html', context)

# Profile Views
@login_required
def profile_view(request):
    return render(request, 'stock/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'stock/profile_update.html', {'form': form})

@login_required
def profile_image_update(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile image updated successfully.")
            return redirect('profile')
    else:
        form = ProfileImageForm(instance=request.user)
    
    return render(request, 'stock/profile_image_update.html', {'form': form})

# Stock Management Views
@login_required
def stock_list(request):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    stock_items = Product.objects.all().order_by('name')
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(stock_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'stock_items': page_obj,
        'categories': categories,
    }
    
    return render(request, 'stock/stock_list.html', context)

@login_required
def stock_detail(request, pk):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    product = get_object_or_404(Product, pk=pk)
    transactions = StockTransaction.objects.filter(product=product).order_by('-timestamp')
    
    context = {
        'product': product,
        'transactions': transactions,
    }
    
    return render(request, 'stock/stock_detail.html', context)

@login_required
def add_stock(request):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            
            # Create initial stock transaction
            StockTransaction.objects.create(
                product=product,
                transaction_type='IN',
                quantity=product.quantity,
                notes=f"Initial stock for {product.name}",
                created_by=request.user
            )
            
            messages.success(request, f"{product.name} added successfully.")
            return redirect('stock_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'suppliers': Supplier.objects.all(),
    }
    
    return render(request, 'stock/add_stock.html', context)

@login_required
def edit_stock(request, pk):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    product = get_object_or_404(Product, pk=pk)
    old_quantity = product.quantity
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save()
            new_quantity = updated_product.quantity
            
            # Create transaction if quantity changed
            if new_quantity != old_quantity:
                transaction_type = 'IN' if new_quantity > old_quantity else 'OUT'
                quantity_change = abs(new_quantity - old_quantity)
                
                StockTransaction.objects.create(
                    product=updated_product,
                    transaction_type=transaction_type,
                    quantity=quantity_change,
                    notes=f"Stock adjustment via edit",
                    created_by=request.user
                )
            
            messages.success(request, f"{updated_product.name} updated successfully.")
            return redirect('stock_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'categories': Category.objects.all(),
        'suppliers': Supplier.objects.all(),
    }
    
    return render(request, 'stock/edit_stock.html', context)

@login_required
def delete_stock(request, pk):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"{product_name} deleted successfully.")
        return redirect('stock_list')
    
    return redirect('stock_detail', pk=pk)

# Category Management
@login_required
def add_category(request):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            
            # Handle AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category': {
                        'id': category.id,
                        'name': category.name
                    }
                })
            
            messages.success(request, f"Category {category.name} added successfully.")
            return redirect('stock_list')
    else:
        form = CategoryForm()
    
    return render(request, 'stock/add_category.html', {'form': form})

# Export to CSV
@login_required
def export_stock_csv(request):
    # Only admin and supervisor can access
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="stock_report_{datetime.date.today()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Category', 'Quantity', 'Unit Price', 'Reorder Level', 'Status'])
    
    products = Product.objects.all()
    for product in products:
        writer.writerow([
            product.id,
            product.name,
            product.category.name,
            product.quantity,
            product.unit_price,
            product.reorder_level,
            'Low Stock' if product.is_low_stock else 'In Stock'
        ])
    
    return response

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta

from stock.models import User
from core.models.product import Product, Category
from core.models.order import Order, OrderItem
from core.decorators import admin_required, supervisor_required

@login_required
def admin_dashboard(request):
    """
    Admin dashboard view showing business overview, stock alerts, and upcoming products.
    """
    # Check if user is admin or supervisor
    if not (request.user.is_admin() or request.user.is_supervisor()):
        messages.error(request, "You don't have permission to access the admin dashboard.")
        return redirect('client_dashboard')
    
    # Get total profit (simplified calculation)
    total_profit = OrderItem.objects.filter(
        order__status__in=['APPROVED', 'SHIPPED', 'DELIVERED']
    ).aggregate(
        profit=Sum(F('quantity') * F('unit_price') * 0.3)  # Assuming 30% profit margin
    )['profit'] or 0
    
    # Get low stock items
    low_stock_items = Product.objects.filter(
        quantity__lte=F('reorder_level')
    ).order_by('quantity')[:5]
    
    # Get upcoming products (products with future expected_date)
    upcoming_products = Product.objects.filter(
        expected_date__gt=timezone.now()
    ).order_by('expected_date')[:5]
    
    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Sales data for chart (last 7 days)
    sales_dates = []
    sales_data = []
    
    for i in range(6, -1, -1):
        date = timezone.now().date() - timedelta(days=i)
        sales_dates.append(date.strftime('%a'))
        
        daily_sales = OrderItem.objects.filter(
            order__created_at__date=date
        ).aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total'] or 0
        
        sales_data.append(daily_sales)
    
    context = {
        'total_profit': total_profit,
        'total_orders': Order.objects.count(),
        'total_products': Product.objects.count(),
        'low_stock_count': Product.objects.filter(quantity__lte=F('reorder_level')).count(),
        'low_stock_items': low_stock_items,
        'upcoming_products': upcoming_products,
        'recent_orders': recent_orders,
        'sales_dates': sales_dates,
        'sales_data': sales_data,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def admin_add_supervisor(request):
    """
    View for admin to add a new supervisor.
    """
    from admin_portal.forms.auth import SupervisorCreationForm
    
    if request.method == 'POST':
        form = SupervisorCreationForm(request.POST)
        if form.is_valid():
            supervisor = form.save()
            messages.success(request, f"Supervisor account for {supervisor.username} created successfully.")
            return redirect('admin_dashboard')
    else:
        form = SupervisorCreationForm()
    
    return render(request, 'admin/add_supervisor.html', {'form': form})

@login_required
@supervisor_required
def admin_reports(request):
    """
    Reports and analytics view for supervisors and admins.
    """
    # Get sales data for the last 30 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Calculate total sales
    total_sales = OrderItem.objects.filter(
        order__created_at__date__range=[start_date, end_date]
    ).aggregate(
        total=Sum(F('quantity') * F('unit_price'))
    )['total'] or 0
    
    # Count orders
    order_count = Order.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).count()
    
    # Calculate average order value
    avg_order_value = total_sales / order_count if order_count > 0 else 0
    
    # Count new customers
    new_customers = User.objects.filter(
        role='CLIENT',
        date_joined__date__range=[start_date, end_date]
    ).count()
    
    # Get top selling products
    top_products = Product.objects.annotate(
        units_sold=Sum('orderitem__quantity'),
        revenue=Sum(F('orderitem__quantity') * F('orderitem__unit_price'))
    ).filter(units_sold__gt=0).order_by('-units_sold')[:5]
    
    # Get sales by category
    categories = Category.objects.annotate(
        sales=Sum(F('product__orderitem__quantity') * F('product__orderitem__unit_price'))
    ).filter(sales__gt=0).order_by('-sales')
    
    category_names = [category.name for category in categories]
    category_sales = [float(category.sales or 0) for category in categories]
    
    # Get sales data for chart (last 30 days)
    sales_dates = []
    sales_data = []
    
    for i in range(29, -1, -1):
        date = end_date - timedelta(days=i)
        sales_dates.append(date.strftime('%d %b'))
        
        daily_sales = OrderItem.objects.filter(
            order__created_at__date=date
        ).aggregate(
            total=Sum(F('quantity') * F('unit_price'))
        )['total'] or 0
        
        sales_data.append(float(daily_sales))
    
    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_sales': total_sales,
        'order_count': order_count,
        'avg_order_value': avg_order_value,
        'new_customers': new_customers,
        'top_products': top_products,
        'categories': categories,
        'category_names': category_names,
        'category_sales': category_sales,
        'sales_dates': sales_dates,
        'sales_data': sales_data,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'admin/reports.html', context)

@login_required
@supervisor_required
def admin_generate_report(request):
    """
    Generate reports based on form parameters.
    """
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        format_type = request.POST.get('format')
        
        # In a real implementation, this would generate the actual report
        # For now, we'll just show a success message
        
        report_names = {
            'sales': 'Sales',
            'inventory': 'Inventory',
            'product': 'Product Performance',
            'customer': 'Customer Analysis'
        }
        
        format_names = {
            'pdf': 'PDF',
            'csv': 'CSV',
            'excel': 'Excel'
        }
        
        report_name = report_names.get(report_type, 'Custom')
        format_name = format_names.get(format_type, 'PDF')
        
        messages.success(request, f"{report_name} Report has been generated in {format_name} format.")
        return redirect('admin_reports')
    
    return redirect('admin_reports')

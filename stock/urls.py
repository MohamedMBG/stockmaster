from django.urls import path
from stock import views
from admin_portal.views.auth import admin_login_view, admin_logout_view
from admin_portal.views.dashboard import admin_dashboard, admin_add_supervisor, admin_reports, admin_generate_report
from client.views.auth import client_login_view, client_register_view, client_logout_view
from client.views.catalog import (
    client_dashboard, client_catalog, client_add_to_cart, client_update_cart, 
    client_remove_from_cart, client_place_order, client_place_order_submit,
    client_orders, client_order_detail
)

urlpatterns = [
    # Original stock views - Updated to use dashboard instead of missing home view
    path('', views.dashboard, name='dashboard'),
    path('login/', client_login_view, name='login'),
    path('register/', client_register_view, name='register'),
    path('logout/', client_logout_view, name='logout'),
    
    # Admin portal views
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-logout/', admin_logout_view, name='admin_logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/add-supervisor/', admin_add_supervisor, name='admin_add_supervisor'),
    path('admin/reports/', admin_reports, name='admin_reports'),
    path('admin/generate-report/', admin_generate_report, name='admin_generate_report'),
    
    # Client views
    path('client/dashboard/', client_dashboard, name='client_dashboard'),
    path('client/catalog/', client_catalog, name='client_catalog'),
    path('client/add-to-cart/', client_add_to_cart, name='client_add_to_cart'),
    path('client/update-cart/', client_update_cart, name='client_update_cart'),
    path('client/remove-from-cart/', client_remove_from_cart, name='client_remove_from_cart'),
    path('client/place-order/', client_place_order, name='client_place_order'),
    path('client/place-order/submit/', client_place_order_submit, name='client_place_order_submit'),
    path('client/orders/', client_orders, name='client_orders'),
    path('client/orders/<int:order_id>/', client_order_detail, name='client_order_detail'),
    
    # Original stock views
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('stock/add/', views.add_stock, name='add_stock'),
    path('stock/<int:pk>/edit/', views.edit_stock, name='edit_stock'),
    path('stock/<int:pk>/delete/', views.delete_stock, name='delete_stock'),
    path('categories/add/', views.add_category, name='add_category'),
    path('export/stock/csv/', views.export_stock_csv, name='export_stock_csv'),
]

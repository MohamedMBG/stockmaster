from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Profile Management
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/image/update/', views.profile_image_update, name='profile_image_update'),
    
    # Admin-only URLs
    path('supervisors/add/', views.add_supervisor, name='add_supervisor'),
    
    # Stock Management
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/<int:pk>/', views.stock_detail, name='stock_detail'),
    path('stock/add/', views.add_stock, name='add_stock'),
    path('stock/<int:pk>/edit/', views.edit_stock, name='edit_stock'),
    path('stock/<int:pk>/delete/', views.delete_stock, name='delete_stock'),
    
    # Category Management
    path('categories/add/', views.add_category, name='add_category'),
    
    # Export
    path('export/stock/csv/', views.export_stock_csv, name='export_stock_csv'),
]

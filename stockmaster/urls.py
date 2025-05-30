from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views  # Add this import
from django.conf import settings
from django.conf.urls.static import static

# Import the admin login view
from admin_portal.views.auth import admin_login_view, admin_logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stock.urls')),
    
    # Custom admin login routes
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-logout/', admin_logout_view, name='admin_logout'),
    
    # Add these password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

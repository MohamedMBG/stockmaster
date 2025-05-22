from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from admin_portal.forms.auth import AdminLoginForm
from core.models.user import User
from core.decorators import admin_required, supervisor_required

def admin_login_view(request):
    """
    Admin login view that accepts only admin@admin.com with password 'admin'
    or supervisors with their credentials.
    """
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Special case for admin@admin.com
            if email == 'admin@admin.com' and password == 'admin':
                # Find or create the admin user
                try:
                    admin_user = User.objects.get(email='admin@admin.com')
                except User.DoesNotExist:
                    # Create admin user if it doesn't exist
                    admin_user = User.objects.create_superuser(
                        email='admin@admin.com',
                        username='admin',
                        password='admin'
                    )
                
                login(request, admin_user)
                messages.success(request, f"Welcome back, Administrator!")
                return redirect('admin_dashboard')
            
            # Regular authentication for supervisors
            user = authenticate(request, username=email, password=password)
            if user is not None and (user.is_admin() or user.is_supervisor()):
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid email or password, or you don't have admin/supervisor privileges.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AdminLoginForm()
    
    return render(request, 'shared/auth/admin_login.html', {'form': form})

@login_required
def admin_logout_view(request):
    """Logout view for admin users."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('admin_login')
